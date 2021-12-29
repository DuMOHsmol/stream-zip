from struct import Struct
import zlib


def stream_zip(files, chunk_size=65536):

    def get_zipped_chunks_uneven():
        local_header_signature = b'\x50\x4b\x03\x04'
        data_descriptor_signature = b'PK\x07\x08'
        directory_header_signature = b'\x50\x4b\x01\x02'
        zip64_size_signature = b'\x01\x00'
        local_file_header_struct = Struct('<H2sHHHIIIHH')
        dir_file_header_struct = Struct('<HH2sHHHIIIHHHHHII')
        directory = []

        offset = 0

        def _(chunk):
            nonlocal offset
            offset += len(chunk)
            yield chunk

        for name, modified_at, chunks in files:
            name_encoded = name.encode()
            local_extra = \
                zip64_size_signature + \
                Struct('<H').pack(16) + \
                Struct('<QQ').pack(0, 0)  # Compressed and uncompressed sizes, 0 since data descriptor
            yield from _(local_header_signature)
            yield from _(local_file_header_struct.pack(
                45,                 # Version
                b'\x08\x00',        # Flags - data descriptor
                8,                  # Compression - deflate
                0,                  # Modification time
                0,                  # Modification date
                0,                  # CRC32 - 0 since data descriptor
                4294967295,         # Compressed size - since zip64
                4294967295,         # Uncompressed size - since zip64
                len(name_encoded),
                len(local_extra),
            ))
            yield from _(name_encoded)
            yield from _(local_extra)

            uncompressed_size = 0
            compressed_size = 0
            crc_32 = zlib.crc32(b'')
            compress_obj = zlib.compressobj(wbits=-zlib.MAX_WBITS, level=9)
            for chunk in chunks:
                uncompressed_size += len(chunk)
                crc_32 = zlib.crc32(chunk, crc_32)
                compressed_chunk = compress_obj.compress(chunk)
                compressed_size += len(compressed_chunk)
                yield from _(compressed_chunk)

            compressed_chunk = compress_obj.flush()
            if compressed_chunk:
                compressed_size += len(compressed_chunk)
                yield from _(compressed_chunk)

            yield from _(data_descriptor_signature)
            yield from _(Struct('<IQQ').pack(crc_32, compressed_size, uncompressed_size))

            directory.append((name_encoded, modified_at, compressed_size, uncompressed_size))

        for name, modified_at, compressed_size, uncompressed_size in directory:
            yield from _(directory_header_signature)
            directory_extra = \
                zip64_size_signature + \
                Struct('<H').pack(16) + \
                Struct('<QQ').pack(compressed_size, uncompressed_size)
            yield from _(dir_file_header_struct.pack(
                45,                 # Version
                45,                 # Version
                b'\x08\x00',        # Flags - data descriptor
                8,                  # Compression - deflate
                0,                  # Modification time
                0,                  # Modification date
                0,                  # CRC32 - 0 since data descriptor
                4294967295,         # Compressed size - since zip64
                4294967295,         # Uncompressed size - since zip64
                len(name_encoded),
                len(directory_extra),
                0,                  # File comment length
                0xffff,             # Disk number - sinze zip64
                0,                  # Internal file attributes - is binary
                0,                  # External file attributes
                0xffffffff,         # Offset of local header - sinze zip64
            ))
            yield from _(name_encoded)
            yield from _(directory_extra)

    def get_zipped_chunks_even(zipped_chunks):
        chunk = b''
        offset = 0
        it = iter(zipped_chunks)

        def up_to(num):
            nonlocal chunk, offset

            while num:
                if offset == len(chunk):
                    try:
                        chunk = next(it)
                    except StopIteration:
                        break
                    else:
                        offset = 0
                to_yield = min(num, len(chunk) - offset)
                offset = offset + to_yield
                num -= to_yield
                yield chunk[offset - to_yield:offset]

        while True:
            block = b''.join(up_to(chunk_size))
            if not block:
                break
            yield block

    zipped_chunks = get_zipped_chunks_uneven()
    yield from get_zipped_chunks_even(zipped_chunks)

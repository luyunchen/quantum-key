
def createKey(key_path):

	import fast_file_encryption as ffe

	from pathlib import Path

	ffe.save_key_pair(public_key=Path(key_path + 'public.pem'), private_key=Path(key_path + 'private.pem'))


def encrypt(from_path, to_path,key_path):

	import fast_file_encryption as ffe

	from pathlib import Path

	original_file = Path(from_path)

	encryptor = ffe.Encryptor(ffe.read_public_key(Path(key_path+'public.pem')))

	encrypted_file = Path(to_path)

	encryptor.copy_encrypted(original_file, encrypted_file, meta={'my-meta': 1}, add_source_metadata=False)


def decrypt(from_path, to_path,key_path):

	import fast_file_encryption as ffe

	from pathlib import Path

	encrypted_file = Path(from_path)
	decryptor = ffe.Decryptor(ffe.read_private_key(Path(key_path+'private.pem')))
	decryptor.copy_decrypted(encrypted_file ,Path(to_path))




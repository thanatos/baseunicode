* I don't think FNV-1A makes a great checksum. Move to SHA-something?
* The checksum is just in hexadecimal. If we could represent it more
  efficiently, it'd be smaller. Maybe ``base64``, for great irony?
* Auto-gzip the input?
* More characters!
* Accents, to push even more data into a character? Multiple accents? Might
  want to be careful of normalization, however.

# calculate_crc32_files.pl

use strict;
use warnings;
use Archive::SevenZip;

my $archive_path = $ARGV[0];

# Открыть архив
my $sevenzip = Archive::SevenZip->new();
$sevenzip->open($archive_path) or die "Ошибка при открытии архива $archive_path: $Archive::SevenZip::LastError\n";

# Получить список файлов в архиве и их CRC32
my @files = $sevenzip->list($archive_path);
foreach my $file (@files) {
    my $crc32 = $sevenzip->extract_hash($archive_path, $file, 'CRC32');
    print "$crc32\n";
}

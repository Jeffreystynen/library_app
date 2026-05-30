// Map of book titles to Open Library cover IDs
// These are actual classic books available on Open Library
const bookCoverMap: Record<string, string> = {
  'Pride and Prejudice': 'OL7919M',
  'Crime and Punishment': 'OL5951711M',
  'Jane Eyre': 'OL7879M',
  'Anna Karenina': 'OL8073M',
  'Wuthering Heights': 'OL7875M',
  'The Brothers Karamazov': 'OL6085M',
  'Great Expectations': 'OL8011M',
  'Frankenstein': 'OL7912M',
  'Twenty Thousand Leagues Under the Sea': 'OL7970M',
  'The Time Machine': 'OL7968M',
  '1984': 'OL7919072M',
  'The Lord of the Rings': 'OL45883M',
  'Brave New World': 'OL7919042M',
  'The Hobbit': 'OL7894M',
  'Murder on the Orient Express': 'OL7968066M',
  'The Girl on the Train': 'OL26316348M',
  'And Then There Were None': 'OL7971M',
  'The Moonstone': 'OL7877M',
  'The Hound of the Baskervilles': 'OL7976M',
  'The Strange Case of Dr. Jekyll and Mr. Hyde': 'OL7982M',
  'Moby Dick': 'OL7943M',
  'The Great Gatsby': 'OL7951M',
  'Emily Dickinson: Selected Poems': 'OL6946256M',
  'The Picture of Dorian Gray': 'OL7985M',
  'Norwegian Wood': 'OL7941395M',
  'One Hundred Years of Solitude': 'OL6076M',
  'Treasure Island': 'OL7973M',
  'Robinson Crusoe': 'OL7883M',
};

export const getBookCoverUrl = (title: string): string => {
  const coverId = bookCoverMap[title];
  if (coverId) {
    return `https://covers.openlibrary.org/b/id/${coverId}-M.jpg`;
  }
  // Fallback to a generic cover image
  return `https://covers.openlibrary.org/b/id/7919M-M.jpg`;
};

// Alternative fallback covers using placeholder service
export const getPlaceholderCover = (_title: string, _author: string): string => {
  return `https://picsum.photos/300/450?random=${Math.random()}`;
};

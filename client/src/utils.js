
export function convertToLocaleTimeString(utcTimestamp) {
  const timestampInMilliseconds = utcTimestamp * 1000;
  const date = new Date(timestampInMilliseconds);
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZoneName: 'short'
  };
  const formattedDateTime = date.toLocaleString(undefined, options);
  return formattedDateTime;
}


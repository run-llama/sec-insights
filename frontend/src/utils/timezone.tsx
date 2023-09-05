export const getDateWithUTCOffset = () => {
  const now = new Date();
  const offsetInMilliseconds = now.getTimezoneOffset() * 60 * 1000;
  const utcDate = new Date(now.getTime() + offsetInMilliseconds);
  return utcDate;
};

export const formatDisplayDate = (dateToDisplay: Date) => {
  // Create a regular expression to match the time portion up to the milliseconds.
  const regex = /(\d{2}:\d{2}:\d{2}\.\d{3})\d*/;

  // Extract the time portion up to the milliseconds.
  const matchedDateTimeString = String(dateToDisplay).replace(regex, "$1");

  // Create a new Date object from the matched string.
  const datetime = new Date(matchedDateTimeString);

  // Convert it to the local time
  datetime.setMinutes(datetime.getMinutes() - datetime.getTimezoneOffset());

  // Get user's timezone
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  // Create an options object for formatting the time.
  const options: Intl.DateTimeFormatOptions = {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
    timeZone: userTimezone, // use the user's timezone
  };

  // Convert the date to the desired format.
  const formattedTime = new Intl.DateTimeFormat("en-US", options).format(
    datetime
  );
  return formattedTime;
};

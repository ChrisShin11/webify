export const getDateTime = () => {
    const date = new Date();
    const formattedDateTime = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
    return formattedDateTime;
  };
  
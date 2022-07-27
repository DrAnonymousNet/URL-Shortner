import { REGEX_URL, REGEX_WHITESPACE, SERVER_DOMAIN } from "../constants";

export const validateURL = (url: string): boolean => {
  let returnValue: boolean;
  try {
    let a = REGEX_URL.test(url);

    returnValue = a && !url.includes(SERVER_DOMAIN);
  } catch (e) {
    returnValue = false;
  }

  return returnValue;
};

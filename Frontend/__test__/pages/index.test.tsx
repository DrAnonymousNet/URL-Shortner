import { fireEvent, render, screen } from "@testing-library/react";
import Index from "../../pages/index";
import { AppWrapper } from "../../context/state";
import App from "next/app";
import axios from "axios";
import { REGEX_URL, SERVER_DOMAIN } from "../../constants";

jest.mock("axios");
const mockedAxios = jest.mocked(axios, true);
describe("Home Page", () => {
  let wrapper: any;
  beforeEach(() => {
    wrapper = render(
      <AppWrapper>
        <Index />
      </AppWrapper>
    );
  });

  it("should not display url length warning", () => {
    expect(wrapper.queryByText(/Sorry/i)).toBeNull();
    expect(wrapper.queryByText(/Here you go/i)).toBeNull();
  });

  it("should display url length warning", () => {
    const input = screen.getByRole("textbox");
    const submitButton = screen.getByRole("button", { name: "Shorten URL" });
    const longURL = new Array(257).join("o");
    fireEvent.change(input, { target: { value: longURL } });
    fireEvent.click(submitButton);

    expect(wrapper.queryByText(/Sorry/i)).not.toBeNull();
  });

  it("should not display url length warning", () => {});

  it("should  allow submission when user enters right URL", () => {
    const submitButton = screen.getByRole("button", { name: "Shorten URL" });
    const valid_URL =
    "https://jkettmann.com/beginners-guide-to-testing-react#react-testing-library-vs-enzyme-vs-jest";
    const input = screen.getByRole("textbox");
    fireEvent.change(input, { target: { value: valid_URL } });
    fireEvent.click(submitButton);
    expect(wrapper.queryByText(/Please , Enter a valid URL/i)).toBeNull();
});

it("should  prevent submission when user enters wrong URLs", () => {
      const submitButton = screen.getByRole("button", { name: "Shorten URL" });
      const invalid_URLs = [
          "https://jkettmann.com/beginners-guide-to-testing-react#react-testing-library-vs-enzyme-vs-jest",
          "//jkettmann.com/beginners-guide-to-testing-react#react-testing-library-vs-enzyme-vs-jest",
          "https://shortenr-api.herokuapp.com/what+is+wrong",
          "htps://www.google.com/?what-on-earth-just-happened"

      ]
      const input = screen.getByRole("textbox");

      invalid_URLs.forEach(url => {
          fireEvent.change(input, { target: { value: url} });
          fireEvent.click(submitButton);
          expect(wrapper.queryByText(/Please , Enter a valid URL/i)).not.toBeNull();
      })
    
  });
});

// mockedAxios.mockImplementationOnce()
// const isURLValid = valid_URL.trim() != '' && REGEX_URL.test(valid_URL) &&
// !valid_URL.includes(SERVER_DOMAIN)
// const invalid_URLs = "https://jkettmann.com/beginners-guide-to-testin g-react#react-testing-library-vs-enzyme-vs-jest"

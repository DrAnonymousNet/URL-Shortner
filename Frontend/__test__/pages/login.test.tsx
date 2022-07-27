import { render,screen } from "@testing-library/react";
import Login from "../../pages/login";
import { AppWrapper } from "../../context/state";

const formLabels = ["Email", "Password"];

describe("Login form", () => {
    let wrapper: any

    beforeEach(() => {
         wrapper = render(
          <AppWrapper>
            <Login />
          </AppWrapper>
        );
    })

  it("should render the form inputs", () => {
    expect(
      wrapper.getByPlaceholderText("JohnDoe@gmail.com")
    ).toBeInTheDocument();
    expect(wrapper.getByPlaceholderText("")).toBeInTheDocument();
  });

  it("should render input labels", () => {
    formLabels.forEach((label) => {
      expect(wrapper.getByLabelText(label)).toBeInTheDocument();
    });
  });

  it("should render log in button" , () => {
    const button = screen.getByRole('button', { name: 'Submit' });
    expect(button).toBeInTheDocument();
    expect(button).not.toBeDisabled();
  } )

  it("should display error when wrong input is enter" , () => {
   
  })
});

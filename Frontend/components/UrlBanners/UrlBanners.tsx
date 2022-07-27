import React from "react";

interface IProps {
  isURLVeryLong: boolean;
  isURLValid: boolean;
  url?: string
}

const UrlBanners = (props: IProps) => {
  return (
    <>
      {props.isURLVeryLong && (
        <p className="border-solid border-[1px] bg-[#fefefe] text-center  rounded-[4px]  text-sm px-6  py-2">
          Sorry, Links longer than 255 characters can&apos;t be shortened yet.
        </p>
      )}
      {!props.isURLValid && props.url && props.url?.length > 0 && (
        <p className="border-solid border-[1px] bg-[#fefefe] text-center  rounded-[4px]  px-6 text-sm py-2">
          Please , enter a valid URL!
        </p>
      )}
    </>
  );
};

export default UrlBanners;

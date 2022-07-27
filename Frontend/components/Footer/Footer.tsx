import Link from "next/link";
import React from "react";

interface IProps {
  fixed: boolean;
}

const Footer = ({ fixed }: IProps) => {
  return (
    <footer
      className={`text-sm text-center pt-16 pb-8 ${
        fixed ? "fixed" : "relative"
      } bottom-0 w-full left-0 z-[10000]`}
    >
      Powered By:{"   "}
      <Link href="https://planetscale.com/" passHref>
        <a
          className="underline underline-offset-2 text-[#2B7FFF] "
          target="_blank"
        >
          Planetscale
        </a>
      </Link>{" "}
      &{"  "}
      <Link href="https://hashnode.com/" passHref>
        <a
          className="underline underline-offset-2 text-[#2B7FFF]"
          target="_blank"
        >
          Hashnode
        </a>
      </Link>
    </footer>
  );
};

export default Footer;

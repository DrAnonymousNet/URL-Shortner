import React, { useEffect, useState } from "react";
import { json } from "stream/consumers";
import { ROW_PER_PAGE } from "../../constants";

interface IProps {
  data: IUserLinks;
  setDataToShow: React.Dispatch<React.SetStateAction<IUserLink[] | undefined>>;
}

const Pagination = ({ data, setDataToShow }: IProps) => {
  const MAX_NUMBER_OF_PAGES = Math.ceil(data.results.length / ROW_PER_PAGE);
  const [currentPage, setCurrentPage] = useState(0);

  const handleButtonClick = (direction: "left" | "right") => {
    if (direction == "left") {
      if (currentPage != 0) {
        setCurrentPage((value) => value - 1);
      }
    }

    if (direction == "right") {
      if (currentPage != MAX_NUMBER_OF_PAGES) {
        setCurrentPage((value) => value + 1);
      }
    }
  };

  useEffect(() => {
    setDataToShow(
      data.results.slice(
        ROW_PER_PAGE * currentPage,
        ROW_PER_PAGE * (currentPage + 1)
      )
    );
  }, [currentPage]);

  console.log("new page number is: ", currentPage);
  return (
    <div className="flex gap-3 justify-center py-2 mt-16 items-center">
      {/* {JSON.stringify(MAX_NUMBER_OF_PAGES)} */}
      <button
        className="mini-btn text-[#fff]  border-[#0B1A30] bg-[#0B1A30]  py-2 px-5 disabled:opacity-25"
        disabled={currentPage == 0}
        onClick={() => handleButtonClick("left")}
      >
        Previous
      </button>

      <p>Page {currentPage + 1}</p>
      <button
        className="mini-btn text-[#fff]  border-[#0B1A30] bg-[#0B1A30]  py-2 px-5 disabled:opacity-25"
        disabled={currentPage + 1 == MAX_NUMBER_OF_PAGES}
        onClick={() => handleButtonClick("right")}
      >
        Next
      </button>
    </div>
  );
};

export default Pagination;

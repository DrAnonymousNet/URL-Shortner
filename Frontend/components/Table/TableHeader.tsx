import React from "react";

const TableHeader = () => {
  return (
    <thead className="bg-[#EBECEF] text-sm">
      <tr className="px-2">
        <th className="max-w-[4/10] pl-2 "> Original Url</th>
        <th className=" ">Short Url</th>
        <th className="w-[1/10] ">Last Date Visited </th>
        <th className="w-[2/10]  text-white pr-2"></th>
      </tr>
    </thead>
  );
};

export default TableHeader;

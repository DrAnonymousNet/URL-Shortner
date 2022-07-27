import React from "react";
import ListItem from "../ListItem/ListItem";
import SubAnalytic from "../SubAnalytic/SubAnalytic";

interface IProps {
  referrers_analytics: IReferrer;
}

const Referrers = ({ referrers_analytics }: IProps) => {
  const total = Object.values(referrers_analytics).reduce(
    (accumulator, value) => accumulator + value,
    0
  );
  return (
    <SubAnalytic
      title="Referrers"
      toolTipMessage="Sites from which visitors visited shortened URL"
    >
      <ul className="flex flex-col gap-3 mt-3  scroll-shadows -mx-2 p-1 w-full  word-break">
        {/* {JSON.stringify(total)} */}
        {JSON.stringify(referrers_analytics) != "{}" ? (
          Object.entries(referrers_analytics).map((referrer, index) => (
            <>
              <ListItem key={index}>
                <div className="flex items-center justify-between w-full gap-2">
                  <span className=" block border-r-[1px]  w-[85%] ">
                    {referrer[0]}
                  </span>
                  <span className="block ">
                    {referrer[1]}
                    {/* {`${Math.round((referrer[1] / total) * 100)}%`} */}
                  </span>
                </div>
              </ListItem>

            </>
          ))
        ) : (
          <p className="text-center text-sm italic">No referrers yet!</p>
        )}
      </ul>
    </SubAnalytic>
  );
};

export default Referrers;

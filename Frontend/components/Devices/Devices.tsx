import React from 'react'
import ListItem from '../ListItem/ListItem';
import SubAnalytic from '../SubAnalytic/SubAnalytic';

interface IProps {
    devices_analytics: IDevice
}

const Devices = ({devices_analytics} : IProps) => {
    return (
        <SubAnalytic
          title="Devices"
          toolTipMessage="Devices on which visitors accessed shortened URL"
        >
          <ul className="flex flex-col gap-3 mt-3 scroll-shadows -mx-2 p-1 w-full  word-break">
            {/* {JSON.stringify(total)} */}
            {JSON.stringify(devices_analytics) != "{}" ? (
              Object.entries(devices_analytics).map((referrer, index) => (
                <>
                <ListItem key={index}>
                  <div className="flex items-center justify-between w-full gap-2">
                    <span className="  block border-r-[1px]  w-[85%] ">
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
              <p className="text-center text-sm italic">No devices yet!</p>
            )}
          </ul>
        </SubAnalytic>
      );
}

export default Devices
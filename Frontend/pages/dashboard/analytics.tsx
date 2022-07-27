import jwtDecode from "jwt-decode";
import React, { useLayoutEffect, useState } from "react";
import MiniCard from "../../components/MiniCard/MiniCard";
import RouteGuard from "../../components/RouteGuard/RouteGuard";
import SubAnalytic from "../../components/SubAnalytic/SubAnalytic";
import Subanalytics from "../../components/SubAnalytics/SubAnalytics";
import ViewBanner from "../../components/ViewBanner/ViewBanner";
import { useAppContext } from "../../context/state";
import useFetchLinks from "../../hooks/useFetchLinks";
import axiosInstance from "../../Services/axios.services";
import dayjs from "dayjs";
import { useRouter } from "next/router";
import { GetServerSideProps } from "next";
import useFetchLink from "../../hooks/useFetchLink";
import DateAnalytics from "../../components/DateAnalytics/DateAnalytics";
import useCopyToClipboard from "../../hooks/useCopyToClipboard";
import Button from "../../components/Button";
import Referrers from "../../components/Referrers/Referrers";
import Devices from "../../components/Devices/Devices";

const Page = () => {
  // console.log
  // const {data} = use
  const router = useRouter();
  // console.log(router.asPath)
  const link_id = router.query.id;
  // console.log(link_id)
  // console.log("userId: " , user_id)
  const {
    state: { email, accessToken, link },
    setState: { setEmail },
  } = useAppContext();
  // console.log(typeof link_id)
  // const user
  // console.log("link Id: " , link)
  // console.log(email)
  // const { data, isLoading, mutate } = useFetchLinks(!!email.length ? email : null)
  const { data, isLoading, mutate, isError } = useFetchLink(link_id as string);
  // console.log(data)
  if (isError && isError.response.status === 403) {
    // console.log(e);
    console.log("Error is : ", isError);
    router.replace("/login");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh");
  }
  // console.log(data)

  useLayoutEffect(() => {
    // console.log(user_id)

    if (accessToken && accessToken != "") {
      const { user_id } = jwtDecode(accessToken) as { user_id: string };

      axiosInstance
        .get(`auth/users/${user_id}/`)
        .then((res) => {
          if (res.status == 200) {
            setEmail(res.data.email);
          }
        })
        .catch((e: any) => {
          if (e.response.status == 401 || e.response.status == 403) {
            console.log(e);
            router.replace("/login");
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh");
          }
        });
      }
    }, [accessToken]);
  //   console.log("date_created is: " , data?.date_created)
  //   console.log("pre-parsed date_created is: " , data?.date_created as string)
  //   console.log("parsed date_created is: " , dayjs(data?.date_created as string))
  //   // console.log("date_created is: " , data?.date_created)
  //   console.log(data?.date_created.split(' ')[0])
  //   console.log(dayjs(data?.date_created.split(' ')[0]))
  // // console.log(data?.analytic.other_analytic)

  return (
    <section className="h-full  w-full  px-5 gap-2 my-5 pb-5">
      {/* bg-[#F9F9FC] */}
      {/* <div className="md:grid gap-y-5"> */}

      <div className=" w-full md:block sm:w-[450px] mx-auto ">
        <MiniCard
          property="Original URL"
          value={data?.long_link as string}
          isLoading={isLoading}
          underline
          truncate
        />

        {/* <div className='col-start-4 col-span-3'> */}

        <MiniCard
          property="Shortened URL"
          value={data?.short_link as string}
          isLoading={isLoading}
          colored
          underline
        />
        {/* </div> */}
        {/* <div className='col-start-7 col-span-2'> */}
        <MiniCard
          property="Date Created"
          value={dayjs(data?.date_created.split(' ')[0] as string).format("MMM D, YYYY")}
          isLoading={isLoading}
        />
        {/* </div> */}
      </div>

      {/* <div className='col-start-5 col-span-4  row-start-2 row-span-2 md:flex justify-around items-center'> */}

      <div className="text-center  flex justify-center mt-8">
        <button
          className=" my-2 mini-btn text-[#fff] py-3  h-[46px] bg-blue-600 px-16 w-max "
          onClick={() => mutate()}
        >
          Refresh
        </button>
      </div>

      <div className=" md:grid grid-cols-12 gap-3 mt-8">
        <div className="col-start-1 col-span-4 w-full ">
          <ViewBanner
            view_count={data ? (data?.visit_count as number).toString() : ""}
            isLoading={isLoading}
          />
        </div>
        <div className="col-start-5 col-span-8 scroll-y-false">
          <DateAnalytics
            isLoading={isLoading}
            date_analytics={
              data
                ? (data?.analytic.date_time_anaylytic as IDateTimeAnalytics)
                : ({} as IDateTimeAnalytics)
            }
          />
        </div>
      </div>

      <Subanalytics
        other_analytics={
          data
            ? (data?.analytic.other_analytic as IOtherAnalytics)
            : ({} as IOtherAnalytics)
        }
        isLoading={isLoading}
      />

      <div className="w-full grid grid-cols-1 md:grid-cols-12 gap-3 my-3 ">
        <div className="col-start-1 col-span-1 md:col-span-4">
          <Referrers
            referrers_analytics={
              data
                ? (data.analytic.other_analytic.Referer as IReferrer)
                : ({} as IReferrer)
            }
          />
        </div>
        <div className="col-start-1 md:col-start-5 md:col-span-4">
          <Devices
            devices_analytics={
              data
                ? (data.analytic.other_analytic.Device as IDevice)
                : ({} as IDevice)
            }
          />
        </div>

        {/* <SubAnalytic
          toolTipMessage="Devices from which visitors accessed shortened link"
          title="Devices"
        >
           <canvas
              id="operatingSystemChart"
              
              className="mx-auto w-full aspect-square max-w-[400px]"
            ></canvas> 
        </SubAnalytic> */}
      </div>
      {/* </div> */}
    </section>
  );
};

export default RouteGuard(Page);

// export async function getStaticPath(){

// }
// export const getServerSideProps: GetServerSideProps = async(context)=>{
//   const { id } = context.query;
//     return{
//         props: {
//           id
//         }
//     }

// }

// // export async function getStaticProps() {
// //     return {
// //       props: {
// //         protected: true,
// //       },
// //     }
// //   }

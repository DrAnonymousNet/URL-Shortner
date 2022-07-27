import axios, { AxiosError } from "axios";
import dayjs from "dayjs";
import jwtDecode from "jwt-decode";
import Link from "next/link";
import Router, { useRouter } from "next/router";
import React, {
  useCallback,
  useDebugValue,
  useEffect,
  useLayoutEffect,
  useState,
} from "react";
import { KeyedMutator, mutate } from "swr";
import Button from "../../components/Button";
import Input from "../../components/Input";
import Loader from "../../components/Loader/Loader";
import Pagination from "../../components/Pagination/Pagination";
import RouteGuard from "../../components/RouteGuard/RouteGuard";
import ShortenedUrlBanner from "../../components/ShortenedUrlBanner/ShortenedUrlBanner";
import Skeleton from "../../components/Skeleton/Skeleton";
import TableHeader from "../../components/Table/TableHeader";
import TableRow from "../../components/Table/TableRow";
import UrlBanners from "../../components/UrlBanners/UrlBanners";
import {
  MAX_URL_CHARACTERS_POSSIBLE,
  REGEX_URL,
  REGEX_WHITESPACE,
  ROW_PER_PAGE,
  SERVER_DOMAIN,
} from "../../constants";
// import { mutate } from 'swr'
import { useAppContext } from "../../context/state";
import { validateURL } from "../../helpers/validateURL";
import useFetchLinks from "../../hooks/useFetchLinks";
import useFetchUser from "../../hooks/useFetchUser";
import axiosInstance from "../../Services/axios.services";

// const isValidURL = REGEX_URL.test(input) && !input.includes(SERVER_DOMAIN) && Boolean(new URL(input))
// setIsURLValid(isValidURL)
// let shouldUpdateDateToShow = true
const Dashboard = () => {
  // const [shouldUpdateDateToShow, setShouldUpdateDateToShow] = useState(true);
  const [isURLVeryLong, setIsURLVeryLong] = useState(false);
  const [isURLValid, setIsURLValid] = useState(true);
  const router = useRouter();
  const {
    state: { accessToken, email },
    setState: { setEmail, setLink },
  } = useAppContext();
  const [isShorteningInProgess, setIsShorteningInProgress] = useState(false);
  // console.log(accessToken)
  const { user_id }: { user_id: string | null } =
    accessToken == "" || !accessToken
      ? { user_id: null }
      : jwtDecode(accessToken);
  const { data, isLoading, mutate, isError } = useFetchLinks(email);
  const SLICE = data?.results.slice(0, ROW_PER_PAGE);
  const [dataToShow, setDataToShow] = useState<IUserLink[] | undefined>(SLICE);
  // console.log()
  // console.log("SLICE is: ", SLICE);
  // console.log("data is:  ", data);
  // console.log(data && data.results.length > 0);
  // console.log("dataToShow is:  ", dataToShow);
  // console.log(isError);
  // console.log(data)

  useEffect(() => {
    if (data && data.results.length > 0) {
      setDataToShow(SLICE);
    }
  }, [data, isLoading]);

  useEffect(() => {
    if (isError && isError.response.status == 401) {
      // console.log("isError oooooo");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh");
      router.replace("/login");
    }
  }, [isError]);
  const [url, setUrl] = useState("");
  const [shortenedUrl, setShortenedUrl] = useState("");

  const handleInput = (e: React.FormEvent) => {
    setShortenedUrl("");
    const { value } = e.target as HTMLInputElement;
    let isValidURL;
    try {
      isValidURL = validateURL(value);
      // console.log("is url valid: ?" , isValidURL)
    } catch (e) {
      isValidURL = false;
    }


    if (value.length > MAX_URL_CHARACTERS_POSSIBLE) {
      setIsURLVeryLong(true);
    } else setIsURLVeryLong(false);

    if (isValidURL) setIsURLValid(true);
    else setIsURLValid(false);

    setUrl(value);
  };

  const handleSubmit = () => {
    // console.log(url.trim().length)
    // const isValidURL = validateURL(url);

    // console.log("is url valid:   ", isValidURL);
    // // setIsURLValid(isValidURL)
    // setIsURLValid(isValidURL);

    if (url.trim().length != 0 && isURLValid && !isURLVeryLong) {
      const formData = {
        long_link: url,
      };
      setIsShorteningInProgress(true);
      axiosInstance
        .post("links/", formData)
        .then((res) => {
          if (res.status == 200 || res.status == 201 || res.status == 208) {
            // console.log(res.data)

            setShortenedUrl(res.data.short_link);
            mutate();
          }
        })
        .catch((e) => console.log("error in dashboard: ", e))
        .finally(() => setIsShorteningInProgress(false));
    }
  };

  useLayoutEffect(() => {
    // console.log(user_id)
    // console.log(accessToken)
    if (accessToken && accessToken != "") {
      axiosInstance
        .get(`auth/users/${user_id}/`)
        .then((res) => {
          if (res.status == 200) {
            setEmail(res.data.email);
          }
        })
        .catch((e: any) => {
          if (e.response.status == 401) {
            console.log("isLayouteffect error.");
            router.replace("/login");
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh");
          }
        });
    }
  }, [accessToken]);

  return (
    <section className=" min-h-screen px-2">
      <div className="w-full px-3 flex flex-col items-center my-14">
        <div className="w-full bg flex flex-col md:flex-row gap-2 my-3 max-w-lg mx-auto md:max-w-5xl md:my-6 items-stretch  ">
          <Input
            className="rounded-[4px] h-[46px] "
            handleChange={(e) => handleInput(e)}
            labelFor="url"
            label=""
            type="text"
            value={url}
            showRedBorder={false}
            placeholder="https://enterthatlongurlyouhaveandgetitshortened.com"
          />
          <button
            className="mini-btn text-[#fff] py-3  border-[#2B7FFF] bg-[#2B7FFF]  md:px-10 flex-shrink-0"
            onClick={handleSubmit}
          >
            Generate short URL
          </button>
          {/* <Button
            classname=" bg-[#2B7FFF] md:w-96 py-3 md:py-0"
            onClick={handleSubmit}
            disabled={isShorteningInProgess}
          >
            Shorten URL
          </Button> */}
        </div>

        {/* UrlBanner shows when user tries to shorten an invalid URL . */}
        <UrlBanners isURLValid={isURLValid} isURLVeryLong={isURLVeryLong} url={url}/>
        {shortenedUrl != "" && !isShorteningInProgess && (
          <ShortenedUrlBanner shortenedUrl={shortenedUrl} />
        )}

        {/* Flag to show when URL length is greater than 255 characters 09999p */}
        {isShorteningInProgess && (
          <div className="mt-3">
            <Loader color="bg-[#0B1A30]" />
          </div>
        )}
      </div>

      <div className="px-3 mt-10 py-5 flex justify-between">
        <p className="font-semibold tracking-wide  text-[#0B1A30] py-1">
          GENERATED LINKS
        </p>

        <p className="text-sm">
          Total:{" "}
          {isLoading ? (
            <Skeleton className="w-4 h-3 inline-block" />
          ) : (
            <span className="text-lg font-semibold">{data?.count}</span>
          )}
        </p>
      </div>

      {/* Table to show when data arrives  */}
      {data && data.results.length > 0 && (
        <div className="w-full  px-3 overflow-x-scroll lg:overflow-x-auto min-h-[651px]">
          <table className="w-full min-w-[900px] px-3 text-left">
            {/* <colgroup>
              <col span={1} className="w-[40%] " />
              <col span={1} className="w-[22%]" />
              <col span={1} className="w-[13%]" />
              <col span={1} className="w-[15%]" />
             
            </colgroup> */}
            <TableHeader />
            <tbody className="text-sm">
              {dataToShow?.map((link, index) => (
                <TableRow link={link} data={data} mutate={mutate} key={index} />
              ))}
              {/* {data?.results?.map((link, index) => (
                <TableRow link={link} data={data} mutate={mutate} />
              ))} */}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination component goes here  */}
      {/* It shows only when there is data and the number of data is > 10 */}
      {data && data.results.length > 10 && (
        <Pagination data={data} setDataToShow={setDataToShow} />
      )}

      {/* Table skeleton to show while data is loading  */}
      {isLoading && <Skeleton className="w-full h-36 " />}

      {/* what appears when there is no shortened links yet  */}
      {data && data.results.length == 0 && (
        <p className="text-center">
          :( Seems you haven&apos;t generated a short link at all.
        </p>
      )}
    </section>
  );
};

export default RouteGuard(Dashboard);

// export async function getStaticProps() {
//   return {
//     props: {
//       protected: true,
//     },
//   }
// }

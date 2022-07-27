import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { BASE_URL } from "../../constants";
import axios from "axios";
import Link from "next/link";
import Loader from "../../components/Loader/Loader";

const Index = ({ uid }: { uid: string[] }) => {
  // console.log(uid)
  const [show, setShow] = useState(false);
  const router = useRouter();
  const [isActivating, setIsActivating] = useState(true);
  const [alreadyActivated, setalreadyActivated] = useState(false);
  const [isSomethingWrong, setIsSomethingWrong] = useState(false);
  // console.log(router.query)
  // const { params } = router.query as {params: string[]}
  // console.log(uid)/
  const formData = {
    uid: uid[0],
    token: uid[1],
  };

  useEffect(() => {
    // .then(res => res.data)
    // console.log("always guarding")
    // setIsActivating(true)
    axios
      .post(BASE_URL + "auth/users/activation/", formData)
      .then((response) => {
        if (response.status == 204 || response.status == 200) {
          setIsActivating(false);
          setalreadyActivated(true);
          setIsSomethingWrong(false);
        }
      })
      .then(() => router.push("/login"))
      .catch((e) => {
        // console.log(e)
        if (e.response.status === 400) {
          setIsSomethingWrong(true);
        }
        if (e.response.status == 403) {
          setalreadyActivated(true);
          setIsActivating(false);
        }
        // console.log(e)
      })
      .finally(() => setIsActivating(false));
  }, []);
  return (
    <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-[#fafefa] w-full text-lg md:px-6 py-4 text-center">
      {isActivating ? (
        <>
          <>
            <Loader color="bg-[#2B7FFF]" />
          </>
          <p>Your account is getting activated. Please wait</p>
        </>
      ) : isSomethingWrong ? (
        <>Seems something went wrong while activating your account! :(</>
      ) : (
        <>
          <p>Your account has been activated successfully.</p>
          <p>
            {" "}
            You can now{" "}
            <span className="underline underline-offset-2 text-[#2B7FFF]">
              <Link href="/login">Log in</Link>
            </span>
          </p>
        </>
      )}
    </div>
  );
};

export default Index;

export const getServerSideProps = async ({ params }: any) => {
  const { uid } = params;

  return {
    props: {
      uid,
    },
  };
};

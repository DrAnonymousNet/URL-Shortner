import axios, { AxiosRequestHeaders, AxiosResponse } from "axios";
import { useContext } from "react";
import { BASE_URL } from "../constants";
// import { useAppContext } from "../context/state";

//  const {state: {accessToken}} = useAppContext()

// let authToken: any

// console.log(this)
// if(  typeof window !== “undefined” && window.localStorage ){
// authToken = localStorage.getItem('access_token') ? JSON.parse(localStorage.getItem('access_token') as string) : null

// }
// console.log(authToken)

const axiosInstance = axios.create({
  baseURL: BASE_URL,
  // headers: {
  //     Authorization: `Bearer ${accessToken}`
  // }
});

axiosInstance.interceptors.request.use(async (req) => {
  //Basically , what to do is :
  // grab stored tokens locally
  //they could  be absent
  //they could have expired
  //they could be present
  //check for their validity
  //if access token is still valid log the user in
  //if valid, proceed with request else dispose them and
  let authToken = localStorage.getItem("access_token")
    ? JSON.parse(localStorage.getItem("access_token") as string)
    : null;
  let refreshToken = localStorage.getItem("refresh")
    ? JSON.parse(localStorage.getItem("refresh") as string)
    : null;

  // if(isValid.status == 401) localStorage.removeItem("refresh")

  // localStorage.setItem("isValid" , is)
  // localStorage.removeItem("isValid")

  if (authToken) {
    try {
      const accessTokenIsValid = await axios.post(
        BASE_URL + "auth/jwt/verify/",
        { token: `${authToken}` }
      );
      console.log(accessTokenIsValid)
      if (req.headers) {
        req.headers.Authorization = `Bearer ${authToken}`;
      }
      return req;
    } catch (error: any) {

      localStorage.removeItem("access_token");
      // if (error.response.status == 401) {
        console.log("daklsf;jak")
        // return req;
      // }
    }
  }
  if (!refreshToken) {
    return req;
  }
  try {
    if (refreshToken) {
      const isValid = await axios.post(BASE_URL + "auth/jwt/verify/", {
        token: `${refreshToken}`,
      });
    }
  } catch (e: any) {
    if (e.response.status == 401) {

      localStorage.removeItem("refresh");
      return req;
    }
  }

  const response = await axios.post(BASE_URL + "auth/jwt/refresh", {
    refresh: JSON.parse(localStorage.getItem("refresh") as string),
  });
  // console.log(refresh)
  localStorage.setItem("access_token", JSON.stringify(response.data.access));

  if (req.headers) {
    req.headers.Authorization = `Bearer ${response.data.access}`;
  }

  // console.log(req)

  return req;
});

export default axiosInstance;

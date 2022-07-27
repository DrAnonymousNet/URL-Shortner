import { useEffect } from "react";
import useSWR, { Fetcher, mutate } from "swr";
import axiosInstance from "../Services/axios.services";

// const fetcher = (url: string,userEmail: string) => axiosInstance.get(url,null,{
//     owner: userEmail
// })


export default function useFetchUser(userId: string | undefined) {
    // let user_id: string
    // if(userId) user_id = userId
    // const fetcher: Fetcher<{ id: number, email: string }, any> = (url: string) => axiosInstance.get(url + user_id).then(res => res.data)

    // // const fetcher: Fetcher<string, User> = (id) => getUserById(id)
    // // const { data, error, mutate } = useSWR(['auth/users/', userId], fetcher)
    // const { data, error, mutate } = useSWR('auth/users/', fetcher)
    // // console.log(data)
    // // useEffect(() => {
    // //     if(data){

    // //         mutate({...data})
    // //     }
    // // }
    // //     , [data])

    // return {
    //     data,
    //     isLoading: !error && !data,
    //     isError: error,
    //     mutate
    // }
}
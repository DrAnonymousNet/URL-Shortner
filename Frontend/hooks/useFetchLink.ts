import { json } from "stream/consumers";
import useSWR, { Fetcher } from "swr";
import axiosInstance from "../Services/axios.services";

// const fetcher = (url: string,userEmail: string) => axiosInstance.get(url,null,{
//     owner: userEmail
// })

export default function useFetchLinks(link_id: string | null){
    // console.log(axiosInstance.head)
    const fetcher: Fetcher<IUserLink,string | null> = (url: string ) => axiosInstance.get(url).then(res => res.data)
    let compare
    let sorteddata;
    console.log(link_id)
    // const fetcher: Fetcher<string, User> = (id) => getUserById(id)
    let duplicate;
    const {data,error,mutate} = useSWR(link_id ? `links/${link_id}/` : link_id, fetcher)
    // console.log(data)
    if(!duplicate || (JSON.stringify(duplicate) !== JSON.stringify(data))){
        duplicate = data
    }
  

    return {
        data: duplicate,
        isLoading: !error && !data,
        isError: error,
        mutate
    }
}
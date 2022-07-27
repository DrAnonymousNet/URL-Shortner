import { json } from "stream/consumers";
import useSWR, { Fetcher } from "swr";
import axiosInstance from "../Services/axios.services";

// const fetcher = (url: string,userEmail: string) => axiosInstance.get(url,null,{
//     owner: userEmail
// })

export default function useFetchLinks(userEmail: string | null){
    const fetcher: Fetcher<IUserLinks,string | null> = (url: string ) => axiosInstance.get(url).then(res => res.data)
    let compare
    let sorteddata;
    // const fetcher: Fetcher<string, User> = (id) => getUserById(id)
    let duplicate;
    const {data,error,mutate} = useSWR(userEmail ? `links/?owner=${userEmail}` : userEmail, fetcher)
    // console.log(data)
    if(!duplicate || (JSON.stringify(duplicate) !== JSON.stringify(data))){
        duplicate = data 
        sorteddata = data
        sorteddata?.results.sort(function(a,b){
            // Turn your strings into dates, and then subtract them
            // to get a value that is either negative, positive, or zero.
            return b.id - a.id;
        })
    }
  

    return {
        data: sorteddata,
        isLoading: !error && !data,
        isError: error,
        mutate
    }
}
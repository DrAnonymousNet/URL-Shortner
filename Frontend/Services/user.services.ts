// import { useAppContext } from "../context/state"
import axiosInstance from "./axios.services"
import { Router, useRouter } from "next/router"
import axios from "axios"
import { BASE_URL } from "../constants"



// const { setState: { setAccessToken, setEmail }, state: { accessToken } } = useAppContext()
// const router = useRouter()

export const login = async (formData: { email: string, password: string }) => {
    return await axios.post(BASE_URL+"auth/jwt/create/", formData)
        .then(res => {
            if (res.status == 200) {

                const { access, refresh } = res.data
                localStorage.setItem("access_token",JSON.stringify(access))
                localStorage.setItem("refresh", JSON.stringify(refresh))
                console.log(res.status)
                return res.data

            }
            // console.log('ahdhdh')
        })

}


type signUpFormData = {
    email: string,
    password: string,
    re_password: string
}

export const signup = async (formData: signUpFormData) => {
    return await axios.post(BASE_URL+"auth/users/", formData)
        .then(response => {

            // console.log(response)
            if (response.status == 201 || response.status == 200) {
                //  }else{
                return

                // console.log(response)
            }
        })

}

export const logout =  () => {
 
     localStorage.removeItem("refresh")
     localStorage.removeItem("access_token")
    
}
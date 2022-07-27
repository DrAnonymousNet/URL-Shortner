import axios, { AxiosResponse } from 'axios'
import Link from 'next/link'
import { useRouter } from 'next/router'
import React, { useEffect, useState } from 'react'
import Button from '../components/Button'
import Input from '../components/Input'
import Loader from '../components/Loader/Loader'
import { BASE_URL } from '../constants'
import { useAppContext } from '../context/state'
import axiosInstance from '../Services/axios.services'
import { login } from '../Services/user.services'

const Login = () => {
  const router = useRouter()
  const [showError,setShowError] = useState(false)
  const { setState: { setAccessToken }, state: { accessToken } } = useAppContext()

  const [isLoggingIn, setIsLoggingIn] = useState(false)

  const [input, setInput] = useState({
    email: '',
    password: '',
  })

  const handleInput = (e: React.FormEvent) => {
    const { name, value } = e.target as HTMLInputElement
    setInput({ ...input, [name]: value })
  }

  const handleSubmit = () => {
    const formData = {
      email: input.email,
      password: input.password
    }
    
    if (input.email != '' || input.password != '') {
      setIsLoggingIn(true)
      login(formData)
        .then(tokens => {
          // console.log(tokens)
        // }
          // if(tokens){
            setShowError(false)
            setAccessToken(tokens.access)
            
            axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${tokens.access}`
            console.log("beforereturnUrl")
            let returnUrl = (router.query.returnUrl as string) || '/dashboard';
            console.log("returnUrl")
            if(returnUrl.includes("/dashboard")){
              returnUrl = "/dashboard"
            }
            // console.log(returnUrl)
          router.push(returnUrl);
          // console.log(accessToken)
        })
        .catch((e: any) => {
          console.log(e)
          if(e.response.status === 401){
            setShowError(true)
          }
        })
        .finally(() => 
        {
          router.query.returnUrl = ''
          setIsLoggingIn(false)
        })
      // axios.post(BASE_URL + "auth/jwt/create/", formData)
      //   .then(res => {
      //     if(res.status == 200){
      //       const {access,refresh} = res.data
      //       axios.defaults.headers.common["Authorization"] = `Bearer ${access}`
      //     }
      //     console.log(res.status)
      //     // console.log('ahdhdh')
      //   })
    }
  }


 

  return (
    <section className='flex items-center justify-center  h-screen'>

      <div className='w-11/12 max-w-[600px] mx-auto flex flex-col gap-4 ' >
        <h1 className='font-bold text-[24px] text-center'>Log In</h1>

        <div className='justify-self-stretch space-y-5'>
          <Input
            className=" text-base pr-3 border-[#C3C0C3] rounded-[4px] h-[46px] "
            label="Email"
            labelFor='email'
            handleChange={handleInput}
            placeholder="JohnDoe@gmail.com"
            showRedBorder={false}
            type="text"

            value={input.email}

          />
          <Input
            className=" text-base pr-3 border-[#C3C0C3] rounded-[4px] h-[46px] "
            label="Password"
            labelFor='password'
            handleChange={handleInput}
            placeholder=""
            //   placeholder="https://Enterthatlongurlandshortenit.com"
            showRedBorder={false}
            type="password"

            value={input.password}

          />
          <div>

          {
            showError 
            &&
            <p className='text-xs text-red-500 '>User doesn&apos;t exist!</p>
          
          }
          <button className='bg-[#0B1A30] my-2 mini-btn text-[#fff] py-3  w-full h-[46px]' onClick={handleSubmit} >
            {
              isLoggingIn
                ?
                <Loader />
                :
                'Submit'
            }
          </button>
            </div>


          <p className='text-center text-sm'>Are you a new user ? {" "}
            <span className='font-bold underline underline-offset-2 '>
              <Link href='/signup'>

                Sign Up
              </Link>
            </span>
          </p>
        </div>

      </div>
    </section>
  )
}

export default Login
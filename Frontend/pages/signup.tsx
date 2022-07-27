import axios from 'axios'
import Link from 'next/link'
import React, { useState } from 'react'
// import { isModuleNamespaceObject } from 'util/types'
import Button from '../components/Button'
import Input from '../components/Input'
import { BASE_URL, REGEX_EMAIL, TIME_ZONE } from '../constants'
import { fieldValidator } from '../helpers/signUpValidator'
import validateForm from '../helpers/validateForm'
import useUser from '../hooks/useFetchLinks'
import Loader from '../components/Loader/Loader'
import { useAppContext } from '../context/state'
import { useRouter } from 'next/router'
import { signup } from '../Services/user.services'
import { format } from 'path'


const Signup = () => {
  const router = useRouter()
  // const {data,isDone,isLoading,mutate} = useUser()
  const {  setState: { setConfirmationEmail } } = useAppContext()
  const [isLoading, setisLoading] = useState(false)
  const [serverResponse, setServerResponse] = useState('')
  const [showEmptyFieldError, setShowEmptyFieldError] = useState(false)
  const [showInputErrors, setShowInputErrors] = useState(false)
  const [input, setInput] = useState<IUser>({
    email: '',
    password: '',
    confirm_password: '',
  })
  const [error, setError] = useState<IUser>({
    email: '',
    password: '',
    confirm_password: ''
  })


  // console.log(error)

  const handleInput = (e: React.FormEvent) => {
    const { name, value } = e.target as HTMLInputElement
    setError({ ...error, [name]: fieldValidator(name, value, input) })
    setInput({ ...input, [name]: value })


  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // console.log(12345678)
    // if
    //  console.log("time-zone is : , " , TIME_ZONE)
    if (input.email == '' || input.confirm_password || input.password) setShowEmptyFieldError(true)

    // console.log(validateForm(error,input))
    if (!validateForm(error, input)) {
      setShowInputErrors(true)
    } else {
      //else block beginning

      setShowInputErrors(false)

      const formData = {
        email: input.email,
        password: input.password,
        re_password: input.confirm_password,
        timezone: TIME_ZONE
      }

      setisLoading(true)
      signup(formData)
        .then(() => {
          setConfirmationEmail(formData.email)
          router.push("/confirmation")
        })
        .catch((err: any) => {

          console.log(err)

          if (err.response && err.response.status == 400) {

            const { email, password } = err.response.data

            if (email) setServerResponse(err.response.data?.email[0])

            else if (password) {

              if (Array.isArray(password)) {
                setServerResponse(password.join("\n"))
              }
            }
            // console.log("error on sign up: ", err)
          }
        })
        .finally(() => setisLoading(false))


      //else block ending
    }
  }


  return (
    <section className='flex items-center justify-center  h-screen'>

      <div className='w-11/12 max-w-[600px] mx-auto flex flex-col gap-4 ' >
        <h1 className='font-bold text-[24px] text-center'>Create an account</h1>

        <div className='justify-self-stretch space-y-5'>
          <div>
            <Input
              className=" text-base pr-3 border-[#C3C0C3] rounded-[4px] h-[46px] "
              label="Email"
              labelFor='email'
              handleChange={handleInput}
              placeholder="JohnDoe@gmail.com"
              showRedBorder={showInputErrors && error.email != ''}
              type="text"


              value={input.email}

            />
            {showInputErrors && error.email != "" && <p className='text-xs text-red-500 '>Enter a valid email !</p>}

          </div>
          <div>

            <Input
              className=" text-base pr-3 border-[#C3C0C3] rounded-[4px] h-[46px] "
              label="Password"
              labelFor='password'
              handleChange={handleInput}
              //   placeholder="https://Enterthatlongurlandshortenit.com"
              showRedBorder={showInputErrors && error.password != ''}
              type="password"

              value={input.password}

            />

            {
              showInputErrors &&
              error.password != '' &&
              <p className='text-xs text-red-500 '>Password must be at least six characters long!</p>
            }

          </div>

          <div>

            <Input
              className=" text-base pr-3 border-[#C3C0C3] rounded-[4px] h-[46px] "
              label="Confirm password"
              labelFor='confirm_password'
              handleChange={handleInput}
              //   placeholder="https://Enterthatlongurlandshortenit.com"
              showRedBorder={showInputErrors && error.confirm_password != ''}
              type="password"

              value={input.confirm_password}

            />
            {
              showInputErrors &&
              error.confirm_password != '' &&
              <p className='text-xs text-red-500 '>Passwords do not match!</p>
            }

          </div>
          <div className='my-2'>

            {serverResponse != '' && <p className='text-xs text-red-500 '>{serverResponse}</p>}
            {/* <Button classname='focus:outline-[#0b1a30] bg-[#0B1A30] text-white mb-2  mt-1' onClick={(e) =>{
              setEmail("haybeecodes@gmail.com")
               router.push('/confirmation')
            }} >
Submit
            </Button> */}
            <button className='bg-[#0B1A30] my-2 mini-btn text-[#fff] py-3  w-full h-[46px]' onClick={(e) => handleSubmit(e)} >
              {
                isLoading ?
                  <Loader /> :
                  "Submit"
              }

            </button>
            <p className='text-center text-sm'>Already have an account ? {" "}
              <span className='font-bold underline underline-offset-2 '>
                <Link href='/login'>

                  Log In
                </Link>
              </span>
            </p>
          </div>
        </div>

      </div>
    </section>
  )
}

export default Signup
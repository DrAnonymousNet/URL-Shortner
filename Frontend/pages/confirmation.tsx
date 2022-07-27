import Link from 'next/link'
import React from 'react'
import { useAppContext } from '../context/state'

const Confirmation = () => {
    const { state: { confirmationEmail } } = useAppContext()
    return (
        <div className='fixed z-[50] top-0 left-0 w-full h-screen text-lg px-6 py-4  text-center bg-[#F9F9FC]/90 flex justify-center items-center'  >
            {
                confirmationEmail == '' ?
                    <div>
                        <p>There is nothing to see here :).</p>
                        <p>Return to <Link href="/">
                        <span className='text-[#2b7fff] cursor-pointer'>
                                Homepage
                            </span>
                        </Link>
                        </p>
                    </div> :
                    <div>
                        <p>

                            A mail has been sent to the email address{" "}
                            <span className='text-[#2B7FFF] '>
                                {confirmationEmail}.
                            </span>
                        </p>
                        <p>

                            Kindly click the link in the mail sent to activate your account.
                        </p>
                    </div>
            }



        </div>
    )
}

export default Confirmation
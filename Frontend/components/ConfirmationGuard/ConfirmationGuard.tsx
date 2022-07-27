import React from 'react'
import { useAppContext } from '../../context/state'

interface IConfirmationGuard {
    children: JSX.Element
}
const ConfirmationGuard = ({children} : IConfirmationGuard) => {
    const {state: {email}} = useAppContext()
    if (email == '') return children
//   return (email == '' && children)
}

export default ConfirmationGuard

import { REGEX_EMAIL}from "../constants"


function fieldValidator(name: string,value: string,input: IUser){
    value = value.trim()
// console.log(value)
    const helper:{[key: string]: string} = {
      // first_name: value == '' &&  value.length == 0 ? 'Enter a valid name' :  '',
      email: REGEX_EMAIL.test(value)  ? '' :   'Enter a valid email please!',
      password:  value.length >= 6 ? '' :  'Password must be at least 6 characters long!',
      confirm_password: input.password === value ? '' : 'Passwords do not matched!'
      // confirm_password: REGEX_PASSWORD.test(value) ? '' :  ,
    }

    return helper[name]
}

export  {fieldValidator}
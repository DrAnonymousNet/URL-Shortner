import axios from "axios";
import { BASE_URL } from "../constants";


export const signup = async ({ email, password, confirm_password }: IUser) => {
    const payload = {
        email,
        password,
        re_password: confirm_password
    }
    try {

        let response = await axios.post<SignUpResponse>(BASE_URL + "/auth/users", payload)


        return  response.data as SignUpResponse
        
        
        // console.log(data)
    } catch (err) {
        console.log("err on signup: ", err)
    }

}

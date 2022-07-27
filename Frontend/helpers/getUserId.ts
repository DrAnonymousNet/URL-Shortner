import jwtDecode from "jwt-decode";

export const getUserId = (accessToken: string): {user_id: string | null} => {
    return  accessToken == "" || !accessToken
    ? { user_id: null }
    : jwtDecode(accessToken);
}
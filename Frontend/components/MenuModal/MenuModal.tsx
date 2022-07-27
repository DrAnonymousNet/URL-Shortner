import { AxiosError } from "axios";
import jwtDecode from "jwt-decode";
import { useRouter } from "next/router";
import React, { useState } from "react";
import { useAppContext } from "../../context/state";
import { getUserId } from "../../helpers/getUserId";
import axiosInstance from "../../Services/axios.services";
import { logout } from "../../Services/user.services";
import Input from "../Input";
import Loader from "../Loader/Loader";

interface IProps {
  setIsModalActive: React.Dispatch<React.SetStateAction<boolean>>;
}

const MenuModal = ({ setIsModalActive }: IProps) => {
  const router = useRouter();
  const {
    state: { accessToken },
  } = useAppContext();
  const [isDeleting, setIsDeleting] = useState(false);
  const { user_id }: { user_id: string | null } = getUserId(accessToken);
  const [password, setPassword] = useState("");
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isWrongPassword, setIsWrongPassword] = useState(false);

  const handleInput = (e: React.FormEvent) => {
    const { value } = e.target as HTMLInputElement;
    setPassword(value);
  };

  const handleFinalDelete = () => {
    console.log("E don cast las las")
    const formData = { current_password: password };
    
    if (password.trim() != "") {
        setIsDeleting(true);
      axiosInstance
        .delete(`auth/users/${user_id}`, { data: formData })
        .then((res) => {
          console.log("response is: ", res);
          if (res.status == 204 || res.status == 200) {
            router.push("/");
            logout();
          }
        })
        .catch((e: any) => {
          if (e.response.status === 400) {
            setIsWrongPassword(true);
          }
        })
        .finally(() => setIsDeleting(false));
    }
  };

  const handleOpenModal = () => {
    setShowDeleteModal((value) => true);
    // setIsModalActive( value => false);
  };

  //   const handleFinalDelete = () => {};

  return (
    <>
      {showDeleteModal && (
        <div
          className="fixed w-full left-0 top-0 h-screen z-50 bg-[#000]/25 flex items-center justify-center"
          onClick={() => setIsModalActive(false)}
        >
          <div
            className="bg-[#fff] p-4 w-[400px] rounded-[4px] "
            onClick={(e) => e.stopPropagation()}
          >
            <p className="text-sm mb-1">Enter your passsword</p>
            <Input
              className=" text-base mb-2 border-[#BD2C00] rounded-[4px] h-[46px]"
              labelFor=""
              handleChange={handleInput}
              placeholder=""
              //   placeholder="https://Enterthatlongurlandshortenit.com"
              showRedBorder={false}
              type="text"
              value={password}
            />
            <div>
              {isWrongPassword && (
                <p className="text-sm text-[#bd2c00]">
                  {" "}
                  Seems you entered a wrong password!
                </p>
              )}
              <button
                className="mini-btn text-[#fff]  border-[#BD2C00] bg-[#BD2C00]  py-3 w-full"
                onClick={() => handleFinalDelete()}
              >
                {
                isDeleting ? (
                  <Loader color="bg-[#FFF]" />
                ) : (
                  "Please, delete my account."
                )}
              </button>
            </div>
          </div>
        </div>
      )}
      <ul className="bg-[#fff] px-4 py-3 ">
        <li>
          <button
            className="mini-btn text-[#fff] hover:text-[#BD2C00] border-[#BD2C00] bg-[#BD2C00]  hover:bg-transparent w-full px-6"
            onClick={() => handleOpenModal()}
            //   onClick={handleLogout}
          >
            Delete Account
            {/* {isDeleting ? <Loader color="bg-[#bd2c00]" /> : "Delete Account"} */}
          </button>
        </li>
      </ul>
    </>
  );
};

export default MenuModal;

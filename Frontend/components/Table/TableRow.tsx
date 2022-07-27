import { AxiosError } from 'axios';
import dayjs from 'dayjs';
import Link from 'next/link';
import { useRouter } from 'next/router';
import React, { useCallback } from 'react'
import { KeyedMutator } from 'swr';
import { useAppContext } from '../../context/state';
import axiosInstance from '../../Services/axios.services';

interface IProps{
    data: IUserLinks | undefined
    link: IUserLink
    mutate: KeyedMutator<IUserLinks>;

}

const TableRow = ({ link,data,mutate}: IProps) => {
    const {setState: {setLink}} = useAppContext()
    const router= useRouter()


    // const TableRow = useCallback(
    //     ({ long_url, short_url, last_visited, id, mutate }: ITableRow) => {
          const handleDelete = (id: number) => {
            axiosInstance
              .delete(`links/${id}`)
              .then((res) => {
                if (res.status == 204) {
                  mutate();
                }
              })
              .catch((e: AxiosError) => {
                // console.log("error on deletion: ", e)
                console.log("this is e: ", e);
                if (e && e?.response?.status == 401) {
                  router.replace("/login");
                  localStorage.removeItem("access_token");
                  localStorage.removeItem("refresh");
                }
              });
          };
          // console.log("last visited date is: ", last_visited);
          return (
            <tr className="border-b-[1px] border-b-[#D9D9D9]">
              <td className="pl-2">{link.long_link}</td>
              <td>{link.short_link}</td>
              <td>
                {link.last_visited_date
                  ? dayjs(link.last_visited_date.split(" ")[0]).format("MMM D, YYYY")
                  : "No visit(s) yet"}
              </td>
              <td className="  basis-16 pr-2 ">
                <div className='flex flex-row-reverse gap-3 mr-0'>
{/* 
                <button
                  className="mini-btn bg-[#F8EAE6] text-[#BD2C00] border-[#bd2c00]  lg:hidden self-stretch"
                  onClick={() => handleDelete(link.id)}
                  >
                  Del
                </button> */}
                <button
                  className="mini-btn bg-[#F8EAE6] text-[#BD2C00] border-[#bd2c00] "
                  onClick={() => handleDelete(link.id)}
                  >
                  Delete
                </button>
                {/* <button
                  className="mini-btn bg-[#F8EAE6] text-[#BD2C00] border-[#bd2c00] md:hidden"
                  onClick={() => handleDelete(link.id)}
                >
                  Del
                </button> */}
                <Link href={`/dashboard/analytics?id=${link.id.toString()}`}>
                  <button
                    className="mini-btn  border-[#2b7fff] bg-[#E6F0FF] text-[#2B7fff] "
                    onClick={() =>
                      setLink(
                          data?.results.find((item) =>item.id == link.id) as IUserLink
                          )
                        }
                        >
                    Analytics
                  </button>
                </Link>
                      </div>
              </td>
            </tr>
          );
    
    //     [data]
    //   );
//   return TableRow
}

export default TableRow
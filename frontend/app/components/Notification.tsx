import React, { useState, useEffect } from "react";
import { Avatar, Dropdown, DropdownItem } from "flowbite-react";

interface NotificationProps {
  itemName: string;
  borrowerID: string;
  location: string;
}

export default function Notification({
  itemName,
  borrowerID,
  location,
}: NotificationProps) {
  const [borrowerDetails, setBorrowerDetails] = useState(null);

  // useEffect(() => {
  //   const fetchUserDetails = async () => {
  //     const body = {
  //       userID: borrowerID,
  //     };
  //     const response = await fetch(
  //       "https://v5ezikbdjg4hadx5mqmundbaxq0zjdnj.lambda-url.ca-central-1.on.aws/",
  //       {
  //         method: "POST",
  //         headers: {
  //           "Content-Type": "application/json",
  //         },
  //         body: JSON.stringify(body),
  //       }
  //     );
  //     const userData = await response.json();
  //     setBorrowerDetails(userData);
  //   };

  //   fetchUserDetails();
  // }, []);

  return (
    <div className="flex bg-brand p-4 border border-gray-700 w-full mx-auto relative">
      <div className="flex">
        <Dropdown
          inline
          label={
            <Avatar
              alt="User settings"
              img="https://flowbite.com/docs/images/people/profile-picture-5.jpg"
              rounded
            />
          }
        >
          <DropdownItem>View Profile</DropdownItem>
        </Dropdown>
      </div>
      <div className="flex-col flex-grow ml-4">
        <p className="text-white text-lg mb-4 pr-4">
          {borrowerID} has Requested your {itemName}!
        </p>
        <div className="flex">
          <button className="px-3 py-2 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-md mr-2">
            Decline
          </button>
          <button className="px-3 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-md">
            Accept
          </button>
        </div>
      </div>
      <div className="top-0 right-0 text-gray-300 text-sm pl-10 pt-1">
        {location} | 1 day ago
      </div>
    </div>
  );
}
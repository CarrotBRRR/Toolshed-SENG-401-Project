import { Textarea } from "flowbite-react";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/utils/authOptions";
import { SuperSession } from "@/app/interfaces/UserI";
import dynamic from "next/dynamic";

const BiographyModal = dynamic(() => import("../BiographyModal"), {
  ssr: false,
});

export default async function Biography({
  bio,
  userID,
}: {
  bio: string;
  userID: string;
}) {
  const session: SuperSession | null = await getServerSession(authOptions);
  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-row justify-between">
        <h1 className="text-xl font-medium">Biography</h1>
        {userID == session?.userData.userID && (
          <BiographyModal bio={session?.userData?.bio} />
        )}
      </div>
      <div className="flex flex-col gap-4 text-black dark:text-white">
        <div className="max-w-md">
          <Textarea
            id="comment"
            placeholder={
              userID == session?.userData.userID ? "Enter a description..." : ""
            }
            rows={12}
            className=" bg-purple-200 text-brand shadow "
            defaultValue={bio}
            disabled={userID != session?.userData.userID}
          />
        </div>
      </div>
    </div>
  );
}

import Link from "next/link";
import { FaTools } from "react-icons/fa";
import { FaHandshake } from "react-icons/fa";
import { FaToolbox } from "react-icons/fa";
import { FaHandHoldingHeart } from "react-icons/fa";

export default function HomePage() {
  return (
    <>
      <div className="h-auto w-full">
        <div className="text-6xl text-center font-extrabold mb-10 animate-pulse ">
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-brand to-teal-400">
            Tools for Everyone, Anywhere.
          </span>
        </div>
        <div className="h-auto w-full flex flex-row justify-evenly items-center">
          <div className="w-1/2 border-r border-brand h-full flex flex-col justify-evenly items-center text-center px-10">
            <div className="text-4xl font-bold underline mb-10">
              Borrow Tools...
            </div>
            <FaTools style={{ fontSize: "7em" }} />
            <div className="text-2xl mt-10">
              Choose a category above to see a list of tools
              <br></br>that are available to be borrowed,
              <br></br>and rent the tool of your choice from one of our lenders!
            </div>
          </div>
          <div className="w-1/2 h-full flex flex-col justify-evenly items-center text-center px-10">
            <div className="text-4xl font-bold underline mb-10">
              ...Or Lend Them!
            </div>
            <FaHandshake style={{ fontSize: "7em" }} />
            <div className="text-2xl mt-10">
              List one of your own tools as available to borrow,
              <br></br>and lend it to someone in need of that tool.
              <br></br>Join our community in its goal of helping others!
            </div>
          </div>
        </div>
        <div className="flex flex-row justify-center items-center mt-10 w-full text-center">
          <Link
            href="/about"
            className="flex justify-center items-center bg-brand font-bold rounded-lg w-fit h-full text-center hover:underline text-4xl px-3 py-3"
          >
            Learn More...
          </Link>
        </div>
      </div>
      <div className="bg-brand mt-28 rounded-md w-full h-full flex flex-row justify-center items-center py-10">
        <div className="w-2/3 text-center h-5/6 pl-10 pr-10">
          <header className="font-bold underline text-2xl mb-8">
            About Us:
          </header>
          <span>
            Welcome to ToolShed, where community and collaboration meet the
            power of shared resources. At ToolShed, we believe that every home
            project is an opportunity to build not just structures but also
            lasting connections within our neighborhoods. Our platform empowers
            users to lend and borrow tools for free, fostering a spirit of
            generosity and cooperation. Whether you are a seasoned DIY
            enthusiast or a first-time fixer-upper, ToolShed is your go-to
            destination for unlocking the potential of community-driven tool
            sharing. Together, let us redefine the way we approach projects and
            create a network of support that transcends the tools themselves,
            creating a true sense of shared accomplishment. Join us in building
            a stronger, more connected community, one borrowed tool at a time.
            Our vision extends beyond the exchange of tools; it encompasses the
            idea that together, we can build something greater than the sum of
            our individual efforts. Let us cultivate a community where
            collaboration is not just a choice but a way of life. Because here,
            we believe that when tools are shared, so too is the joy of creating
            and building a better world, one tool at a time.
          </span>
        </div>
        <div className="w-1/3 text-center h-5/6 flex justify-center items-center">
          <FaToolbox style={{ fontSize: "15em" }} />
        </div>
      </div>

      <div className="bg-brand mt-28 rounded-md w-full h-full flex flex-row justify-center items-center py-10">
        <div className="w-1/3 text-center h-5/6 flex justify-center items-center">
          <FaHandHoldingHeart style={{ fontSize: "15em" }} />
        </div>
        <div className="w-2/3 text-center h-5/6 pl-10 pr-10">
          <header className="font-bold underline text-2xl mb-8">
            Our Goal:
          </header>
          <span>
            At ToolShed, our goal is to cultivate a vibrant and interconnected
            community through the power of sharing. We believe that every tool
            has a story to tell and a purpose to serve, and by fostering a
            platform where users can lend and borrow tools for free, we aim to
            create a collaborative environment that transcends the
            transactional. ToolShed is not just a platform; it is a
            community-driven initiative promoting generosity, trust, and mutual
            support. Through sharing tools, we empower our users to connect,
            learn, and collaborate on various projects. Moreover, we strive to
            extend our reach beyond mere tool transactions, incorporating a
            charitable dimension by encouraging users to donate unused tools to
            those in need, building a stronger, more compassionate community one
            tool at a time. Join ToolShed, where tools become the catalyst for
            meaningful connections and positive change. Embrace the spirit of
            giving, innovation, and camaraderie with ToolShed, where every
            borrowed drill, saw, or wrench represents a step toward a more
            connected, compassionate world. Start sharing, start caring - let us
            work our hardest today so that we may build a better tomorrow!
          </span>
        </div>
      </div>
    </>
  );
}

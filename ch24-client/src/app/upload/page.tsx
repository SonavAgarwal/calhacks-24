"use client"

import { FileUp } from "lucide-react"
import React, { useState } from "react"
import Image from "next/image"
import Dropzone from "react-dropzone"
import { twMerge } from "tailwind-merge"

interface Props {}

const page = (props: Props) => {
    const [uploadType, setUploadType] = useState<"inventory" | "claims">(
        "inventory",
    )

    const [files, setFiles] = useState<File[]>([])

    const handleDrop = (acceptedFiles: File[]) => {
        setFiles((prev) => [...prev, ...acceptedFiles])
    }

    return (
        <div className="flex min-h-screen w-full flex-col items-center justify-center gap-4 p-4">
            {/* <h1 className="text-4xl font-bold w-full">Upload Media</h1> */}

            {/* two tabs called "inventory" and "for claims" */}
            {/* the selected one is black background white text */}
            {/* the background should slide between the two options, like a pill */}

            <div className="relative flex w-64 rounded-full bg-background">
                {/* Sliding background */}
                <div
                    className={twMerge(
                        "absolute bottom-0 left-1 top-0 my-1 rounded-full bg-black transition-all duration-300",
                        uploadType === "inventory"
                            ? "w-1/2"
                            : "-left-1 w-1/2 translate-x-full",
                        "outline-none",
                    )}
                ></div>

                {/* Inventory Button */}
                <button
                    className={twMerge(
                        "relative z-10 flex-1 rounded-full py-2 text-center",
                        uploadType === "inventory"
                            ? "text-white"
                            : "text-black",
                        "outline-none transition-colors",
                    )}
                    onClick={() => setUploadType("inventory")}
                >
                    Inventory
                </button>

                {/* For Claims Button */}
                <button
                    className={twMerge(
                        "relative z-10 flex-1 rounded-full py-2 text-center",
                        uploadType === "claims" ? "text-white" : "text-black",
                        "outline-none transition-colors",
                    )}
                    onClick={() => setUploadType("claims")}
                >
                    For Claims
                </button>
            </div>

            <Dropzone
                onDrop={(acceptedFiles) => handleDrop(acceptedFiles)}
                accept={{
                    "image/png": [".png"],
                    "image/jpeg": [".jpg"],
                    "image/heic": [".heic"],
                    "video/mp4": [".mp4"],
                }}
            >
                {({ getRootProps, getInputProps }) => (
                    <div
                        className="flex h-96 w-96 flex-col items-center justify-center rounded-xl bg-background p-4"
                        {...getRootProps()}
                    >
                        <input {...getInputProps()} />
                        {files.length === 0 && (
                            <>
                                <Image
                                    width={100}
                                    height={100}
                                    src="/assets/upload-cards.png"
                                    alt="upload cards"
                                    className="mb-4"
                                />
                                <p className="text-center text-xl font-bold">
                                    Upload photos and videos
                                </p>
                                <p className="text-center italic">
                                    .png, .jpg, .heic, .mp4
                                </p>
                            </>
                        )}
                        {files.length > 0 && (
                            <div className="grid h-full w-full grid-cols-2 gap-4 overflow-auto rounded-xl bg-background">
                                {files.map((file, i) => (
                                    <div
                                        key={i}
                                        className="relative rounded-xl"
                                    >
                                        <img
                                            src={URL.createObjectURL(file)}
                                            alt={`uploaded file ${i}`}
                                            className="rounded-xl object-cover"
                                        />
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </Dropzone>

            <div className="flex w-96 justify-center gap-4">
                <button
                    className="flex-1 rounded-xl bg-background px-4 py-2 text-black"
                    onClick={() => setFiles([])}
                >
                    Clear
                </button>
                <button
                    className="flex-1 rounded-xl bg-primary px-4 py-2 text-white"
                    onClick={() => console.log(files)}
                >
                    Upload
                </button>
            </div>
        </div>
    )
}

export default page

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
        setFiles(acceptedFiles)
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

            {files.length === 0 && (
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
                        </div>
                    )}
                </Dropzone>
            )}

            {/* show images and videos */}
            <div className="mt-4 grid grid-cols-3 gap-4">
                {files.map((file, i) => (
                    <div
                        key={i}
                        className="relative h-32 w-32 rounded-xl bg-background p-2"
                    >
                        <img
                            src={URL.createObjectURL(file)}
                            alt={`uploaded file ${i}`}
                            className="h-full w-full rounded-xl object-cover"
                        />
                    </div>
                ))}
            </div>
        </div>
    )
}

export default page

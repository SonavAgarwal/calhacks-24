import { Image } from "@/lib/types"
import { useEffect } from "react"

export default function ImageDialog({
    enlargedImage,
    setEnlargedImage,
}: {
    enlargedImage: Image | null
    setEnlargedImage: (image: Image | null) => void
}) {
    // Close the dialog on Escape key press
    useEffect(() => {
        const handleEscape = (event: KeyboardEvent) => {
            if (event.key === "Escape") {
                setEnlargedImage(null)
            }
        }
        window.addEventListener("keydown", handleEscape)
        return () => window.removeEventListener("keydown", handleEscape)
    }, [setEnlargedImage])

    // Close the dialog on click outside the image
    const handleDialogClick = (e: React.MouseEvent) => {
        setEnlargedImage(null)
    }

    return (
        <div
            className={`fixed inset-0 z-[400] flex items-center justify-center bg-black bg-opacity-50 transition-opacity duration-300 ${
                enlargedImage ? "opacity-100" : "pointer-events-none opacity-0"
            }`}
            onClick={handleDialogClick}
            style={{ transitionProperty: "opacity" }}
        >
            {enlargedImage && (
                <img
                    src={enlargedImage.url}
                    alt={enlargedImage.id}
                    className="max-h-full max-w-full"
                />
            )}
        </div>
    )
}

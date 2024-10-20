import { Item } from "@/lib/types"
import React from "react"

interface Props {
    item: Item
}

const ItemCard = ({ item }: Props) => {
    return (
        <div className="flex gap-4 rounded-lg bg-background p-4">
            <h1>{item.name}</h1>
            <p>{item.price}</p>
            <p>{item.quantity}</p>
            <p>{item.categories.join(", ")}</p>
            <p>{item.dateUpdated.toISOString()}</p>
            <div>
                {item.images.map((image, index) => (
                    <img key={index} src={image} alt={item.name} />
                ))}
            </div>
        </div>
    )
}

export default ItemCard

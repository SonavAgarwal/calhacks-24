import {
    CellContext,
    ColumnDef,
    createColumnHelper,
} from "@tanstack/react-table"

export interface Item {
    id: string
    name: string
    description: string
    price: string
    before_count: number
    category: string
    images: Image[]
    // before_images: Image[]
    // after_images: Image[]
}

export interface Image {
    image_id: string
    url_path: string
    status: "pending" | "inventory" | "rejected" | "matched"
    before: boolean
}

export interface Claim {
    id: number
    name: string
    dateFiled: Date
    items: Item[]
}

export interface UploadSessionResponse {
    id: string
    date: Date
    after: boolean
    processing: boolean
    items: Item[]
}

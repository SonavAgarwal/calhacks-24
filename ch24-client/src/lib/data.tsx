import { Claim, Item } from "./types"

export const PLACEHOLDER_ITEMS: Item[] = [
    {
        id: "1",
        name: "Placeholder Item 1",
        description: "This is a placeholder description for item 1.",
        price: "10.99",
        before_count: 5,
        category: "Category 1",
        images: [
            {
                image_id: "1a",
                url_path: "https://picsum.photos/seed/1a/200",
                status: "inventory",
                before: true,
            },
            {
                image_id: "1b",
                url_path: "https://picsum.photos/seed/1b/200",
                status: "pending",
                before: true,
            },
        ],
    },
    {
        id: "2",
        name: "Placeholder Item 2",
        description: "This is a placeholder description for item 2.",
        price: "15.49",
        before_count: 2,
        category: "Category 2",
        images: [
            {
                image_id: "2a",
                url_path: "https://picsum.photos/seed/2a/200",
                status: "rejected",
                before: true,
            },
        ],
    },
    {
        id: "3",
        name: "Placeholder Item 3",
        description: "This is a placeholder description for item 3.",
        price: "9.99",
        before_count: 10,
        category: "Category 1",
        images: [
            {
                image_id: "3a",
                url_path: "https://picsum.photos/seed/3a/200",
                status: "inventory",
                before: true,
            },
            {
                image_id: "3b",
                url_path: "https://picsum.photos/seed/3b/200",
                status: "pending",
                before: false,
            },
        ],
    },
    {
        id: "4",
        name: "Placeholder Item 4",
        description: "This is a placeholder description for item 4.",
        price: "25.0",
        before_count: 7,
        category: "Category 3",
        images: [
            {
                image_id: "4a",
                url_path: "https://picsum.photos/seed/4a/200",
                status: "inventory",
                before: true,
            },
            {
                image_id: "4b",
                url_path: "https://picsum.photos/seed/4b/200",
                status: "pending",
                before: false,
            },
            {
                image_id: "4c",
                url_path: "https://picsum.photos/seed/4c/200",
                status: "rejected",
                before: false,
            },
        ],
    },
    {
        id: "5",
        name: "Placeholder Item 5",
        description: "This is a placeholder description for item 5.",
        price: "5.75",
        before_count: 3,
        category: "Category 2",
        images: [
            {
                image_id: "5a",
                url_path: "https://picsum.photos/seed/5a/200",
                status: "inventory",
                before: true,
            },
        ],
    },
    {
        id: "6",
        name: "Placeholder Item 6",
        description: "This is a placeholder description for item 6.",
        price: "12.49",
        before_count: 6,
        category: "Category 1",
        images: [
            {
                image_id: "6a",
                url_path: "https://picsum.photos/seed/6a/200",
                status: "inventory",
                before: true,
            },
            {
                image_id: "6b",
                url_path: "https://picsum.photos/seed/6b/200",
                status: "pending",
                before: true,
            },
        ],
    },
    {
        id: "7",
        name: "Placeholder Item 7",
        description: "This is a placeholder description for item 7.",
        price: "8.99",
        before_count: 8,
        category: "Category 4",
        images: [
            {
                image_id: "7a",
                url_path: "https://picsum.photos/seed/7a/200",
                status: "rejected",
                before: false,
            },
            {
                image_id: "7b",
                url_path: "https://picsum.photos/seed/7b/200",
                status: "inventory",
                before: true,
            },
        ],
    },
    {
        id: "8",
        name: "Placeholder Item 8",
        description: "This is a placeholder description for item 8.",
        price: "19.95",
        before_count: 12,
        category: "Category 3",
        images: [
            {
                image_id: "8a",
                url_path: "https://picsum.photos/seed/8a/200",
                status: "inventory",
                before: true,
            },
        ],
    },
    {
        id: "9",
        name: "Placeholder Item 9",
        description: "This is a placeholder description for item 9.",
        price: "29.99",
        before_count: 1,
        category: "Category 5",
        images: [
            {
                image_id: "9a",
                url_path: "https://picsum.photos/seed/9a/200",
                status: "inventory",
                before: true,
            },
            {
                image_id: "9b",
                url_path: "https://picsum.photos/seed/9b/200",
                status: "pending",
                before: true,
            },
            {
                image_id: "9c",
                url_path: "https://picsum.photos/seed/9c/200",
                status: "rejected",
                before: false,
            },
        ],
    },
    {
        id: "10",
        name: "Placeholder Item 10",
        description: "This is a placeholder description for item 10.",
        price: "4.99",
        before_count: 15,
        category: "Category 2",
        images: [
            {
                image_id: "10a",
                url_path: "https://picsum.photos/seed/10a/200",
                status: "inventory",
                before: true,
            },
        ],
    },
]

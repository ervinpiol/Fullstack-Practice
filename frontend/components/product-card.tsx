"use client";

import Image from "next/image";
import { Card, CardContent } from "@/components/ui/card";
import { Star } from "lucide-react";

interface ProductCardProps {
  id: string;
  name: string;
  price: number;
  image: string;
  rating: number;
  reviews: number;
  onClick: () => void;
  stock: number;
}

export function ProductCard({
  name,
  price,
  image,
  rating,
  reviews,
  onClick,
  stock,
}: ProductCardProps) {
  return (
    <Card
      onClick={onClick}
      className="group overflow-hidden cursor-pointer transition-all hover:shadow-lg hover:scale-105 p-0"
    >
      <CardContent className="p-0">
        <div className="relative w-full aspect-square bg-muted overflow-hidden">
          <Image
            src={"/premium-wireless-headphones.png"}
            alt={name}
            fill
            className="object-cover group-hover:scale-110 transition-transform duration-300"
          />
        </div>
        <div className="p-4 space-y-3">
          <h3 className="font-semibold text-foreground line-clamp-2">
            {name}{" "}
            {stock === 0 && (
              <span className="text-neutral-600">(Sold Out)</span>
            )}
          </h3>
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1">
              <Star className="w-4 h-4 fill-primary text-primary" />
              <span className="text-sm font-medium text-foreground">
                {rating}
              </span>
            </div>
            <span className="text-xs text-muted-foreground">({reviews})</span>
          </div>
          <div
            className={`text-lg font-bold text-primary ${
              stock === 0 && "line-through"
            }`}
          >
            ${price.toFixed(2)}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

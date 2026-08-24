import Image from "next/image";
import { gallery, type GalleryItem } from "@/lib/site";
import { PhotoPlaceholder } from "@/components/ui";

const sizeClass: Record<NonNullable<GalleryItem["size"]>, string> = {
  lg: "col-span-2 row-span-2",
  wide: "col-span-2",
  tall: "row-span-2",
  sm: "",
};

/* Volgorde tegelt exact in het 4-koloms grid (en in 2 kolommen op mobiel):
   lg(2×2) + tall(1×2) + sm + sm vullen rij 1–2; wide(2×1) + sm + sm rij 3. */
const placeholderPlan: { label: string; size: GalleryItem["size"] }[] = [
  { label: "Skin fade — zijkant", size: "lg" },
  { label: "Fade — achterkant", size: "tall" },
  { label: "Lineup — close-up", size: "sm" },
  { label: "Baard trim — resultaat", size: "sm" },
  { label: "Cut + baard combo", size: "wide" },
  { label: "Kids cut", size: "sm" },
  { label: "Fresh voor het weekend", size: "sm" },
];

/** Mondriaan-galerij: asymmetrische blokken met 1px goudlijnen ertussen. */
export function Gallery({ limit }: { limit?: number }) {
  const items = gallery.slice(0, limit);
  const placeholders = placeholderPlan.slice(0, limit ?? placeholderPlan.length);

  return (
    <div className="grid auto-rows-[9rem] grid-cols-2 gap-px border border-gold/20 bg-gold/20 sm:auto-rows-[11rem] sm:grid-cols-4">
      {items.length > 0
        ? items.map((item) => (
            <figure
              key={item.src}
              className={`group relative overflow-hidden bg-surface ${sizeClass[item.size ?? "sm"]}`}
            >
              <Image
                src={item.src}
                alt={item.alt}
                fill
                sizes="(max-width: 640px) 50vw, 25vw"
                className="object-cover transition-transform duration-500 group-hover:scale-[1.03]"
              />
              <figcaption className="display absolute bottom-0 left-0 bg-ink/80 px-2 py-1 text-[10px] text-olive-bright opacity-0 transition-opacity group-hover:opacity-100">
                {item.style}
              </figcaption>
            </figure>
          ))
        : placeholders.map((p) => (
            <PhotoPlaceholder
              key={p.label}
              label={p.label}
              className={`border-0 ${sizeClass[p.size ?? "sm"]}`}
            />
          ))}
    </div>
  );
}

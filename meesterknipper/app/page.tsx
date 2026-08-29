import BookingFlow from "@/components/BookingFlow";
import { SALON } from "@/lib/data";

export default function Home() {
  return (
    <div>
      <section className="mb-8 text-center">
        <h1 className="text-3xl font-extrabold tracking-tight">
          Boek je afspraak <span className="text-gold-400">online</span>
        </h1>
        <p className="mt-2 text-sm text-zinc-400">
          {SALON.name} · di t/m za 09:00–18:00 · {SALON.address}
        </p>
      </section>
      <BookingFlow />
    </div>
  );
}

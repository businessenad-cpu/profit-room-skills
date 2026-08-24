import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "Kapper Sint Niklaas — Kom binnen. Ga fresh naar buiten.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OgImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: 80,
          background: "#0e0e0b",
          color: "#f4f1e6",
          fontFamily: "sans-serif",
        }}
      >
        <div style={{ display: "flex", color: "#c6a250", fontSize: 40 }}>
          ✂ KAPPER SINT NIKLAAS
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            marginTop: 30,
            fontSize: 88,
            fontWeight: 800,
            lineHeight: 1.05,
            textTransform: "uppercase",
          }}
        >
          <span>Kom binnen.</span>
          <span style={{ color: "#a6bd5a" }}>Ga fresh naar buiten.</span>
        </div>
        <div style={{ display: "flex", marginTop: 40, fontSize: 32, color: "#d9c9a3" }}>
          Ankerstraat 61B · Sint-Niklaas · Boek online
        </div>
        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            right: 0,
            height: 14,
            background: "#7a8b3f",
            display: "flex",
          }}
        />
      </div>
    ),
    { ...size },
  );
}

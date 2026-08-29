import { SALON, type Barber, type Service } from "./data";
import { formatDateNL, formatPrice } from "./format";
import type { Booking } from "./store";

export type EmailPreview = {
  to: string;
  subject: string;
  html: string;
};

export type EmailResult = {
  demoMode: boolean;
  sent: boolean;
  error?: string;
  customerEmail: EmailPreview;
  salonEmail: EmailPreview | null;
};

export function buildCustomerEmail(
  booking: Booking,
  service: Service,
  barber: Barber
): EmailPreview {
  const date = formatDateNL(booking.date, true);
  return {
    to: booking.customerEmail,
    subject: `✂️ Je afspraak bij ${SALON.name} is bevestigd — ${formatDateNL(booking.date)} ${booking.time}`,
    html: `
<div style="background:#0a0a0b;padding:32px 16px;font-family:Helvetica,Arial,sans-serif;color:#f4f4f5;">
  <div style="max-width:520px;margin:0 auto;background:#1a1a1d;border:1px solid #2e2e33;border-radius:16px;overflow:hidden;">
    <div style="background:#121214;padding:24px;text-align:center;border-bottom:2px solid #d9ad2b;">
      <div style="font-size:22px;font-weight:bold;color:#eec84f;">✂️ ${SALON.name}</div>
      <div style="color:#a1a1aa;margin-top:4px;font-size:14px;">Je afspraak is bevestigd</div>
    </div>
    <div style="padding:24px;">
      <p style="margin:0 0 16px;">Hoi ${booking.customerName},</p>
      <p style="margin:0 0 20px;color:#d4d4d8;">Bedankt voor je boeking. Dit zijn de details van je afspraak:</p>
      <table style="width:100%;border-collapse:collapse;font-size:15px;">
        <tr><td style="padding:8px 0;color:#a1a1aa;">Boekingsnummer</td><td style="padding:8px 0;text-align:right;font-weight:bold;color:#eec84f;">${booking.id}</td></tr>
        <tr><td style="padding:8px 0;color:#a1a1aa;border-top:1px solid #2e2e33;">Dienst</td><td style="padding:8px 0;text-align:right;border-top:1px solid #2e2e33;">${service.name}</td></tr>
        <tr><td style="padding:8px 0;color:#a1a1aa;border-top:1px solid #2e2e33;">Kapper</td><td style="padding:8px 0;text-align:right;border-top:1px solid #2e2e33;">${barber.name}</td></tr>
        <tr><td style="padding:8px 0;color:#a1a1aa;border-top:1px solid #2e2e33;">Datum &amp; tijd</td><td style="padding:8px 0;text-align:right;border-top:1px solid #2e2e33;">${date}, ${booking.time}</td></tr>
        <tr><td style="padding:8px 0;color:#a1a1aa;border-top:1px solid #2e2e33;">Prijs</td><td style="padding:8px 0;text-align:right;font-weight:bold;border-top:1px solid #2e2e33;">${formatPrice(booking.price)}</td></tr>
        <tr><td style="padding:8px 0;color:#a1a1aa;border-top:1px solid #2e2e33;">Adres</td><td style="padding:8px 0;text-align:right;border-top:1px solid #2e2e33;">${SALON.address}</td></tr>
      </table>
      <p style="margin:24px 0 0;padding:12px 16px;background:#121214;border-radius:8px;color:#d4d4d8;font-size:14px;">
        Kun je niet komen? Zeg minimaal 24 uur vooraf af.
      </p>
    </div>
    <div style="padding:16px 24px;border-top:1px solid #2e2e33;text-align:center;color:#71717a;font-size:12px;">
      Powered by <strong style="color:#eec84f;">Knipklok</strong> — online boeken voor kapsalons
    </div>
  </div>
</div>`.trim(),
  };
}

export function buildSalonEmail(
  booking: Booking,
  service: Service,
  barber: Barber,
  salonEmail: string
): EmailPreview {
  const date = formatDateNL(booking.date, true);
  return {
    to: salonEmail,
    subject: `Nieuwe boeking: ${booking.customerName} — ${service.name} bij ${barber.name} op ${formatDateNL(booking.date)} ${booking.time}`,
    html: `
<div style="font-family:Helvetica,Arial,sans-serif;font-size:15px;color:#18181b;">
  <p><strong>Nieuwe boeking via Knipklok</strong> (${booking.id})</p>
  <ul>
    <li>Klant: ${booking.customerName} — ${booking.customerPhone} — ${booking.customerEmail}</li>
    <li>Dienst: ${service.name} (${formatPrice(booking.price)}, ${booking.durationMin} min)</li>
    <li>Kapper: ${barber.name}</li>
    <li>Wanneer: ${date}, ${booking.time}</li>
    ${booking.note ? `<li>Opmerking: ${booking.note}</li>` : ""}
  </ul>
</div>`.trim(),
  };
}

export async function sendBookingEmails(
  booking: Booking,
  service: Service,
  barber: Barber
): Promise<EmailResult> {
  const customerEmail = buildCustomerEmail(booking, service, barber);
  const salonAddress = process.env.SALON_EMAIL;
  const salonEmail = salonAddress
    ? buildSalonEmail(booking, service, barber, salonAddress)
    : null;

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.log("=== DEMO-MODUS: geen RESEND_API_KEY, mail wordt niet verstuurd ===");
    console.log(`Aan: ${customerEmail.to}`);
    console.log(`Onderwerp: ${customerEmail.subject}`);
    console.log(customerEmail.html);
    if (salonEmail) {
      console.log(`--- Salonnotificatie aan: ${salonEmail.to} ---`);
      console.log(`Onderwerp: ${salonEmail.subject}`);
      console.log(salonEmail.html);
    }
    return { demoMode: true, sent: false, customerEmail, salonEmail };
  }

  try {
    const { Resend } = await import("resend");
    const resend = new Resend(apiKey);
    const from = process.env.EMAIL_FROM || "Kapper Sint Niklaas <onboarding@resend.dev>";

    const results = await Promise.allSettled([
      resend.emails.send({
        from,
        to: customerEmail.to,
        subject: customerEmail.subject,
        html: customerEmail.html,
      }),
      ...(salonEmail
        ? [
            resend.emails.send({
              from,
              to: salonEmail.to,
              subject: salonEmail.subject,
              html: salonEmail.html,
            }),
          ]
        : []),
    ]);

    const failures = results.filter(
      (r) => r.status === "rejected" || (r.status === "fulfilled" && r.value.error)
    );
    if (failures.length > 0) {
      console.error("Resend fout:", failures);
      return {
        demoMode: false,
        sent: false,
        error: "Mail versturen mislukte (boeking is wel opgeslagen).",
        customerEmail,
        salonEmail,
      };
    }
    return { demoMode: false, sent: true, customerEmail, salonEmail };
  } catch (err) {
    console.error("Resend fout:", err);
    return {
      demoMode: false,
      sent: false,
      error: "Mail versturen mislukte (boeking is wel opgeslagen).",
      customerEmail,
      salonEmail,
    };
  }
}

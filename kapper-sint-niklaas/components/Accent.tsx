/**
 * Rendert tekst waarin *woorden tussen sterretjes* het olijfgroene accent
 * krijgen en \n een regeleinde wordt — zo kan de AI-assistent/beheerder
 * accenten leggen zonder HTML te schrijven.
 */
export function Accent({ text }: { text: string }) {
  return (
    <>
      {text.split("\n").map((line, li) => (
        <span key={li}>
          {li > 0 && <br />}
          {line.split("*").map((part, pi) =>
            pi % 2 === 1 ? (
              <span key={pi} className="text-olive-bright">
                {part}
              </span>
            ) : (
              <span key={pi}>{part}</span>
            ),
          )}
        </span>
      ))}
    </>
  );
}

async function askCaptain() {

    const question =
        document.getElementById(
            "question"
        ).value;

    const language =
        document.getElementById(
            "language"
        ).value;

    const resultElement =
        document.getElementById(
            "result"
        );

    resultElement.innerText =
        "Processing...";

    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question:
                            question,

                        target_language:
                            language
                    })
                }
            );

        if (!response.ok) {

            throw new Error(
                "Request failed"
            );
        }

        const data =
            await response.json();

        resultElement.innerText =

            "Retrieved Sources:\n" +

            data.retrieved_documents
                .map(
                    doc =>
                        doc.source
                )
                .join("\n") +

            "\n\nLLM Answer:\n" +

            data.answer +

            "\n\nTranslation:\n" +

            data.translation +

            "\n\nProcessing Time: " +

            data.processing_time +

            " seconds";

        const audio =
            document.getElementById(
                "audio"
            );

        audio.src =
            data.audio +

            "?t=" +

            Date.now();

        audio.load();

        audio.play();

    }

    catch (error) {

        resultElement.innerText =
            "Error: " +
            error.message;

    }

}
"""Interactive script for learning German irregular verbs."""

import random
import sys
from typing import Dict, Any
import click

from german_verbs.verbs import load_verb_data


class VerbLearner:
    """Class for learning and practicing German verb forms."""

    def __init__(self, yaml_file: str):
        """Initialize the learner with a YAML file."""
        self.data = load_verb_data(yaml_file)
        self.verbs = self.data["verbs"]
        self.correct_answers = 0
        self.total_questions = 0
        self.question_types = [
            self._question_infinitive_to_forms,
            self._question_prateritum_to_forms,
            self._question_partizip_to_forms,
            self._question_english_to_forms,
            self._question_ukrainian_to_forms,
        ]

    def _question_infinitive_to_forms(self, verb: Dict[str, Any]) -> bool:
        """Ask for Präteritum and Partizip II given the infinitive."""
        infinitive = verb["infinitiv"]
        correct_prateritum = verb["präteritum"]
        correct_partizip = verb["partizip"]

        click.echo(f"\nGiven the infinitive: {infinitive}")
        click.echo("Type '?' for help at any prompt")
        
        prateritum = click.prompt("What is the Präteritum form?")
        if prateritum == '?':
            self._show_verb_help(verb)
            return self._question_infinitive_to_forms(verb)
        
        partizip = click.prompt("What is the Partizip II form?")
        if partizip == '?':
            self._show_verb_help(verb)
            return self._question_infinitive_to_forms(verb)

        prateritum_correct = prateritum.lower() == correct_prateritum.lower()
        partizip_correct = partizip.lower() == correct_partizip.lower()

        if prateritum_correct and partizip_correct:
            click.echo(click.style("Correct!", fg="green", bold=True))
            return True
        else:
            click.echo(click.style("Incorrect!", fg="red", bold=True))
            if not prateritum_correct:
                click.echo(f"The correct Präteritum is: {correct_prateritum}")
            if not partizip_correct:
                click.echo(f"The correct Partizip II is: {correct_partizip}")
            return False

    def _question_prateritum_to_forms(self, verb: Dict[str, Any]) -> bool:
        """Ask for Infinitive and Partizip II given the Präteritum."""
        infinitive = verb["infinitiv"]
        prateritum = verb["präteritum"]
        correct_partizip = verb["partizip"]

        click.echo(f"\nGiven the Präteritum: {prateritum}")

        answer_infinitive = click.prompt("What is the infinitive form?")
        answer_partizip = click.prompt("What is the Partizip II form?")

        infinitive_correct = answer_infinitive.lower() == infinitive.lower()
        partizip_correct = answer_partizip.lower() == correct_partizip.lower()

        if infinitive_correct and partizip_correct:
            click.echo(click.style("Correct!", fg="green", bold=True))
            return True
        else:
            click.echo(click.style("Incorrect!", fg="red", bold=True))
            if not infinitive_correct:
                click.echo(f"The correct infinitive is: {infinitive}")
            if not partizip_correct:
                click.echo(f"The correct Partizip II is: {correct_partizip}")
            return False

    def _question_partizip_to_forms(self, verb: Dict[str, Any]) -> bool:
        """Ask for Infinitive and Präteritum given the Partizip II."""
        infinitive = verb["infinitiv"]
        correct_prateritum = verb["präteritum"]
        partizip = verb["partizip"]

        click.echo(f"\nGiven the Partizip II: {partizip}")

        answer_infinitive = click.prompt("What is the infinitive form?")
        answer_prateritum = click.prompt("What is the Präteritum form?")

        infinitive_correct = answer_infinitive.lower() == infinitive.lower()
        prateritum_correct = (answer_prateritum.lower() ==
                              correct_prateritum.lower())

        if infinitive_correct and prateritum_correct:
            click.echo(click.style("Correct!", fg="green", bold=True))
            return True
        else:
            click.echo(click.style("Incorrect!", fg="red", bold=True))
            if not infinitive_correct:
                click.echo(f"The correct infinitive is: {infinitive}")
            if not prateritum_correct:
                click.echo(f"The correct Präteritum is: {correct_prateritum}")
            return False

    def _question_english_to_forms(self, verb: Dict[str, Any]) -> bool:
        """Ask for German forms given the English translation."""
        infinitive = verb["infinitiv"]
        correct_prateritum = verb["präteritum"]
        correct_partizip = verb["partizip"]
        english = verb["translations"]["english"]

        click.echo(f"\nGiven the English translation: {english}")

        answer_infinitive = click.prompt("What is the infinitive form?")
        answer_prateritum = click.prompt("What is the Präteritum form?")
        answer_partizip = click.prompt("What is the Partizip II form?")

        infinitive_correct = answer_infinitive.lower() == infinitive.lower()
        prateritum_correct = (answer_prateritum.lower() ==
                              correct_prateritum.lower())
        partizip_correct = (answer_partizip.lower() ==
                            correct_partizip.lower())

        all_correct = (infinitive_correct and prateritum_correct and
                       partizip_correct)

        if all_correct:
            click.echo(click.style("Correct!", fg="green", bold=True))
            return True
        else:
            click.echo(click.style("Incorrect!", fg="red", bold=True))
            if not infinitive_correct:
                click.echo(f"The correct infinitive is: {infinitive}")
            if not prateritum_correct:
                click.echo(f"The correct Präteritum is: {correct_prateritum}")
            if not partizip_correct:
                click.echo(f"The correct Partizip II is: {correct_partizip}")
            return False

    def _question_ukrainian_to_forms(self, verb: Dict[str, Any]) -> bool:
        """Ask for German forms given the Ukrainian translation."""
        infinitive = verb["infinitiv"]
        correct_prateritum = verb["präteritum"]
        correct_partizip = verb["partizip"]
        ukrainian = verb["translations"]["ukrainian"]

        click.echo(f"\nGiven the Ukrainian translation: {ukrainian}")
        click.echo("Type '?' for help at any prompt")

        answer_infinitive = click.prompt("What is the infinitive form?")
        if answer_infinitive == '?':
            self._show_verb_help(verb)
            return self._question_ukrainian_to_forms(verb)

        answer_prateritum = click.prompt("What is the Präteritum form?")
        if answer_prateritum == '?':
            self._show_verb_help(verb)
            return self._question_ukrainian_to_forms(verb)

        answer_partizip = click.prompt("What is the Partizip II form?")
        if answer_partizip == '?':
            self._show_verb_help(verb)
            return self._question_ukrainian_to_forms(verb)

        infinitive_correct = (answer_infinitive.lower() == infinitive.lower())
        prateritum_correct = (answer_prateritum.lower() ==
                              correct_prateritum.lower())
        partizip_correct = (answer_partizip.lower() ==
                            correct_partizip.lower())

        all_correct = (infinitive_correct and prateritum_correct and
                       partizip_correct)

        if all_correct:
            click.echo(click.style("Correct!", fg="green", bold=True))
            return True
        else:
            click.echo(click.style("Incorrect!", fg="red", bold=True))
            if not infinitive_correct:
                click.echo(f"The correct infinitive is: {infinitive}")
            if not prateritum_correct:
                click.echo(f"The correct Präteritum is: {correct_prateritum}")
            if not partizip_correct:
                click.echo(f"The correct Partizip II is: {correct_partizip}")
            return False

    def ask_random_question(self) -> None:
        """Ask a random question about a random verb."""
        verb = random.choice(self.verbs)
        question_function = random.choice(self.question_types)

        self.total_questions += 1
        is_correct = question_function(verb)
        if is_correct:
            self.correct_answers += 1

    def run_practice_session(self) -> None:
        """Run an interactive practice session."""
        click.echo(click.style("=== German Verb Practice ===", bold=True))
        click.echo(f"Loaded {len(self.verbs)} verbs from {self.data['title']}")
        click.echo("Press Ctrl+C at any time to end the session "
                   "and see your statistics.")

        try:
            while True:
                self.ask_random_question()

                # Show current stats
                correct = self.correct_answers
                total = self.total_questions
                percentage = (correct / total) * 100
                msg = f"Current score: {correct}/{total} "
                msg += f"({percentage:.1f}%)"
                click.echo(msg)
                click.echo("-" * 30)

                # Ask if user wants to continue
                prompt = "Continue with another question?"
                if not click.confirm(prompt, default=True):
                    break

        except KeyboardInterrupt:
            click.echo("\nPractice session interrupted.")

        self.show_statistics()

    def show_statistics(self) -> None:
        """Show the statistics of the practice session."""
        click.echo("\n" + "=" * 50)
        click.echo(click.style("Practice Session Statistics", bold=True))
        click.echo("=" * 50)

        if self.total_questions == 0:
            click.echo("No questions were answered.")
            return

        percentage = (self.correct_answers / self.total_questions) * 100

        click.echo(f"Total questions: {self.total_questions}")
        click.echo(f"Correct answers: {self.correct_answers}")
        click.echo(f"Accuracy: {percentage:.1f}%")

        # Give some feedback based on performance
        if percentage >= 90:
            msg = "\nExcellent job! You're mastering these verbs!"
            click.echo(click.style(msg, fg="green", bold=True))
        elif percentage >= 70:
            msg = "\nGood work! Keep practicing to improve further."
            click.echo(click.style(msg, fg="green"))
        elif percentage >= 50:
            msg = "\nNot bad, but there's room for improvement. Keep going!"
            click.echo(click.style(msg, fg="yellow"))
        else:
            msg = "\nKeep practicing! Learning these verbs takes time."
            click.echo(click.style(msg, fg="red"))

    def _show_verb_help(self, verb: Dict[str, Any]) -> None:
        """Display full information about a verb as help."""
        click.echo("\n" + "=" * 50)
        click.echo(click.style("Verb Help", fg="blue", bold=True))
        click.echo("=" * 50)
        
        # Display basic info
        click.echo(f"Infinitive: {verb['infinitiv']} ({verb['person3']})")
        click.echo(f"Präteritum: {verb['präteritum']}")
        click.echo(f"Partizip II: {verb['partizip']}")
        click.echo(f"English: {verb['translations']['english']}")
        click.echo(f"Ukrainian: {verb['translations']['ukrainian']}")
        
        # Display examples if available
        if verb.get("examples"):
            click.echo("\nExamples:")
            click.echo(verb["examples"])
        
        click.echo("\n" + "=" * 50)
        click.echo("Press Enter to continue...")
        input()  # Wait for user to press Enter


@click.command()
@click.argument("yaml_file", default="irregular-verbs-a1.yaml")
@click.option(
    "--question-limit", "-n",
    default=0,
    help="Number of questions to ask (0 for unlimited)"
)
@click.option(
    "--mode", "-m",
    type=click.Choice([
        "random", "infinitive", "prateritum",
        "partizip", "english", "ukrainian"
    ]),
    default="random",
    help="Practice mode - which type of questions to ask"
)
def learn(yaml_file, question_limit, mode):
    """Learn German irregular verbs through interactive practice.

    Provide a YAML_FILE path to use a specific verb list.
    """
    learner = VerbLearner(yaml_file)

    # Filter question types based on mode
    if mode != "random":
        # Select only the specific question type
        mode_map = {
            "infinitive": 0,
            "prateritum": 1,
            "partizip": 2,
            "english": 3,
            "ukrainian": 4
        }

        if mode in mode_map:
            idx = mode_map[mode]
            learner.question_types = [learner.question_types[idx]]

    try:
        if question_limit > 0:
            click.echo(f"Practice session with {question_limit} questions")
            click.echo(f"Learning mode: {mode}")

            for _ in range(question_limit):
                try:
                    learner.ask_random_question()
                except KeyboardInterrupt:
                    break

            learner.show_statistics()
        else:
            learner.run_practice_session()
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    learn()

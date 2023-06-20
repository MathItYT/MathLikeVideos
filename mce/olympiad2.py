"""Problema: Para $a$, $b$, $c$ enteros, resuelva el siguiente
sistema de ecuaciones:
\\begin{align*}
a + bc &= 2020\\\\
c + ab &= 2021
\\end{align*}"""


import manim as mn
from azure_speech_scene import AzureSpeechScene
from logo import Logo
from math_creature import MathCreature, RoundBubble, ShowBubble, DestroyBubble


mn.config["background_color"] = "#333333"
SYSTEM = "a+bc&=2020\\\\c+ab&=2021"
MATHTEX_SYSTEM = mn.MathTex(
    SYSTEM,
    substrings_to_isolate=["a", "b", "c", "2020", "2021"],
    font_size=72
).set_color_by_tex_to_color_map({
    "a": mn.BLUE_D,
    "b": mn.BLUE,
    "c": mn.BLUE_B,
    "2020": mn.LIGHTER_GREY,
    "2021": mn.LIGHTER_GREY
})
RESUELVE = (
    "\\text{Encuentre todos los }",
    "a", ",", "b", ",", "c", "\\in", 
    "\\mathbb{Z}"
)
MATHTEX_RESUELVE = mn.MathTex(
    *RESUELVE,
    font_size=80,
    tex_environment="equation*"
)
MATHTEX_RESUELVE[1].set_color(mn.BLUE_D)
MATHTEX_RESUELVE[3].set_color(mn.BLUE)
MATHTEX_RESUELVE[5].set_color(mn.BLUE_B)
MATHTEX_RESUELVE[7].set_color(mn.LIGHTER_GREY)


class Thumbnail(mn.Scene):
    def construct(self):
        logo = Logo().to_corner(mn.DR)
        en_menos_de_5_min = mn.Tex(
            "En menos de 5 minutos",
            font_size=66
        ).to_edge(mn.DOWN)
        youtube = mn.SVGMobject("youtube.svg").scale(0.5)
        youtube[0].set_color(mn.WHITE)
        youtube[1].set_color(mn.PURE_RED)
        youtube_logo = Logo(mn.PURE_RED, youtube).to_corner(mn.DL)
        self.add(
            MATHTEX_RESUELVE.to_edge(mn.UP),
            MATHTEX_SYSTEM,
            en_menos_de_5_min,
            youtube_logo,
            logo
        )


class ElEjercicio(Thumbnail, AzureSpeechScene):
    def construct(self):
        super().construct()
        self.express_as("affectionate")
        resuelve, system, en_menos_de_5_min, youtube_logo, logo \
            = self.mobjects
        self.remove(*self.mobjects)
        resuelve_vg = mn.VGroup(*[
            subpart for part in resuelve
            for subpart in part
        ])
        with self.voiceover("Dados los enteros a, b, c, resuelva el siguiente sistema de ecuaciones."):
            self.play(mn.AddTextLetterByLetter(resuelve_vg))
            self.wait()
            self.play(mn.LaggedStartMap(mn.FadeIn, system, shift=0.5 * mn.UP))
        with self.voiceover("Lo resolveremos en menos de 5 minutos. ¡Vamos a la obra!"):
            self.play(mn.Write(en_menos_de_5_min))
            self.play(mn.SpinInFromNothing(youtube_logo))
            self.play(mn.SpinInFromNothing(logo))
        creature = MathCreature().to_corner(mn.DR)
        self.remove(logo)
        self.add(creature)
        self.play(mn.FadeIn(creature.eyes))
        self.play(creature.blink())
        self.wait()
        with self.voiceover("Pensemos en cómo será nuestra estrategia."):
            self.play(
                mn.ShrinkToCenter(youtube_logo, path_arc=mn.PI / 2),
                mn.FadeOut(en_menos_de_5_min)
            )
            self.play(creature.eyes.anim_look_at(system))
            self.play(creature.blink())
        eq1 = system[:6]
        eq2 = system[6:]
        with self.voiceover("Notemos que hay una solución trivial. Si b es igual a 0, entonces c es igual a 2020 y a es igual a 2021."):
            bc = eq1[1:4]
            ab = eq2[2:5]
            self.play(mn.VGroup(bc, ab).animate.set_opacity(0.1))
            self.play(creature.blink())
        with self.voiceover("Pero posiblemente haya otras soluciones, así que haremos deducciones a partir de esto para llegar a todas las soluciones."):
            self.play(mn.VGroup(bc, ab).animate.set_opacity(1))
            self.play(creature.blink())
        with self.voiceover("Daré vuelta las ecuaciones y quiero que notes algo."):
            self.play(mn.Swap(eq1, eq2, path_arc=mn.PI))
            self.play(creature.blink())
        tips = mn.VGroup(mn.StealthTip(), mn.StealthTip())
        tip1, tip2 = tips
        tip1.next_to(eq2, mn.RIGHT).flip()
        tip2.next_to(eq1, mn.RIGHT).flip()
        with self.voiceover(
            "Ese 2021 y ese 2020 se distancian en una unidad. Eso se obtiene restando el 2021 con el 2020, así que la estrategia" \
                + " será restar las ecuaciones y factorizar el lado izquierdo. Intenta adivinar qué sigue."
        ):
            self.play(
                mn.LaggedStartMap(
                    mn.FadeIn,
                    tips,
                    scale=2,
                    lag_ratio=0.5
                ),
            )
            self.play(creature.blink())
            self.wait()
            difference = mn.MathTex(
                "2021", "-", "2020", "=", "1",
                font_size=72
            ).next_to(system, mn.DOWN)
            difference[::2].set_color(mn.LIGHTER_GREY)
            eq2021, eq2020 = mn.VGroup(
                mn.MathTex("2021").replace(eq2[-1]),
                mn.MathTex("2020").replace(eq1[-1])
            )
            self.play(mn.TransformMatchingTex(
                mn.VGroup(eq2021, eq2020),
                difference,
                path_arc=-mn.PI
            ))
            self.play(mn.FadeOut(tips))
            self.play(creature.blink())
        lab_dot = mn.LabeledDot("-")
        lab_dot.next_to(system, mn.LEFT)
        with self.voiceover("Restamos las ecuaciones tal como había dicho."):
            self.play(mn.Write(lab_dot))
            self.play(creature.blink())
            self.wait()
            self.play(mn.FadeOut(difference))
        
        resta_system = mn.MathTex(
            "c", "+", "a", "b", "-",
            "(", "a", "+", "b", "c", ")",
            "=", "1",
            font_size=72
        )
        resta_system.set_color_by_tex_to_color_map({
            "a": mn.BLUE_D,
            "b": mn.BLUE,
            "c": mn.BLUE_B,
            "1": mn.LIGHTER_GREY
        })
        resta_system.next_to(system, mn.DOWN)
        with self.voiceover("Hay que desarrollar el lado izquierdo, te encargo a ti la tarea de hacerlo."):
            self.play(mn.TransformMatchingTex(
                system.copy(), resta_system,
                path_arc=mn.PI
            ))
            self.play(creature.eyes.anim_look_at(resta_system))
            self.play(mn.FadeOut(lab_dot))
            self.play(creature.blink())
        factor = mn.MathTex(
            "(", "b", "-", "1", ")", "(", "a", "-", "c", ")",
            "=", "1",
            font_size=72
        )
        factor.set_color_by_tex_to_color_map({
            "a": mn.BLUE_D,
            "b": mn.BLUE,
            "c": mn.BLUE_B,
            "1": mn.LIGHTER_GREY
        })
        factor.next_to(system, mn.DOWN)
        with self.voiceover("Si lo hiciste bien, deberías haber obtenido esto."):
            self.play(mn.TransformMatchingTex(
                resta_system, factor
            ))
            creature.eyes.anim_look_at(factor)
            self.play(creature.blink())
        al_estar_en_Z = mn.Tex(
            "\\textbf{Teorema:} Dados $x,y\\in\\mathbb{Z}$," \
                + " si $xy=1$,\\\\entonces o bien $x=y=1$" \
                + " o bien $x=y=-1$.",
            font_size=36
        )
        bubble = RoundBubble(
            al_estar_en_Z,
            bubble_start=creature.get_corner(mn.UL),
            direction=mn.UL,
            flip=mn.UP
        )
        system_and_factor = mn.VGroup(system, factor)
        with self.voiceover("Notemos que b menos 1 es entero y a menos c es entero, y ese producto de enteros es igual a 1. Así que usaremos este teorema."):
            self.play(mn.FadeOut(system_and_factor))
            self.play(ShowBubble(bubble))
            self.play(creature.blink())
        with self.voiceover("Así que ambos factores están obligados o bien a ser 1 o bien a ser menos 1."):
            self.play(DestroyBubble(bubble))
            self.play(mn.FadeIn(system_and_factor))
            self.play(creature.blink())

        factors_equal1 = mn.MathTex(
            "b", "-", "1", "&=", "1\\\\",
            "a", "-", "c", "&=", "1",
            font_size=72
        )
        factors_equal1.set_color_by_tex_to_color_map({
            "a": mn.BLUE_D,
            "b": mn.BLUE,
            "c": mn.BLUE_B,
            "1": mn.LIGHTER_GREY
        })
        factors_equal_minus1 = mn.MathTex(
            "b", "-", "1", "&=", "-1\\\\",
            "a", "-", "c", "&=", "-1",
            font_size=72
        )
        factors_equal_minus1.set_color_by_tex_to_color_map({
            "a": mn.BLUE_D,
            "b": mn.BLUE,
            "c": mn.BLUE_B,
            "1": mn.LIGHTER_GREY
        })
        factors_equal = mn.VGroup(factors_equal1, factors_equal_minus1)
        factors_equal.arrange(mn.RIGHT, buff=2)
        factors_equal.to_edge(mn.DOWN)
        with self.voiceover("Entonces esto se separa en los dos casos."):
            self.play(mn.TransformMatchingTex(
                factor, factors_equal
            ))
            self.play(creature.blink())
        expressed_another_way1 = mn.MathTex(
            "b", "&=", "2\\\\",
            "a", "&=", "c", "+", "1",
            font_size=72
        )
        expressed_another_way1.set_color_by_tex_to_color_map({
            "a": mn.BLUE_D,
            "b": mn.BLUE,
            "c": mn.BLUE_B,
            "1": mn.LIGHTER_GREY
        })
        expressed_another_way_minus1 = mn.MathTex(
            "b", "&=", "0\\\\",
            "a", "&=", "c", "-", "1",
            font_size=72
        )
        expressed_another_way_minus1.set_color_by_tex_to_color_map({
            "a": mn.BLUE_D,
            "b": mn.BLUE,
            "c": mn.BLUE_B,
            "1": mn.LIGHTER_GREY
        })
        expressed_another_way = mn.VGroup(
            expressed_another_way1,
            expressed_another_way_minus1
        )
        expressed_another_way.arrange(mn.RIGHT, buff=2)
        expressed_another_way.to_edge(mn.DOWN)
        with self.voiceover("Trabajando los términos, obtenemos esto."):
            self.play(
                mn.TransformMatchingTex(
                    factors_equal1, expressed_another_way1
                ),
                mn.TransformMatchingTex(
                    factors_equal_minus1, expressed_another_way_minus1
                )
            )
            self.play(creature.blink())
            self.wait()
            self.play(mn.FadeOut(resuelve))
        with self.voiceover("Notemos que el segundo caso es la solución trivial."):
            self.play(system.animate.to_edge(mn.UP))
            self.play(creature.eyes.anim_look_at(system))
            self.play(creature.blink())
        with self.voiceover("Porque considerando el sistema, podemos directamente sustituir b por 0."):         
            self.play(mn.Indicate(system))
            self.wait()
            second_case = mn.MathTex(
                "a", "&=", "2020\\\\",
                "b", "&=", "0\\\\",
                "c", "&=", "2021",
                font_size=72
            )
            second_case.set_color_by_tex_to_color_map({
                "a": mn.BLUE_D,
                "b": mn.BLUE,
                "c": mn.BLUE_B,
                "1": mn.LIGHTER_GREY
            })
            second_case.next_to(system, mn.DOWN)
            rec = mn.SurroundingRectangle(second_case)
            self.play(mn.DrawBorderThenFill(second_case))
            self.play(mn.Create(rec))
            self.play(creature.eyes.anim_look_at(second_case))
            self.play(creature.blink())

        first_case = mn.MathTex(
            "a", "-", "1", "+", "2", "a", "&=", "2021\\\\",
            "b", "&=", "2\\\\",
            "c", "+", "1", "+", "2", "c", "&=", "2020",
            font_size=60
        )
        first_case.set_color_by_tex_to_color_map({
            "a": mn.BLUE_D,
            "b": mn.BLUE,
            "c": mn.BLUE_B,
            "1": mn.LIGHTER_GREY,
            "2": mn.LIGHTER_GREY,
            "2021": mn.LIGHTER_GREY,
            "2020": mn.LIGHTER_GREY
        })
        first_case.to_edge(mn.RIGHT)
        with self.voiceover("Ahora vamos con el primero. Te encargo a ti resolver estas ecuaciones lineales para obtener a y c."):
            self.play(mn.VGroup(second_case, rec).animate.scale(5 / 6).to_edge(mn.LEFT))
            self.play(mn.DrawBorderThenFill(first_case))
            self.play(creature.eyes.anim_look_at(first_case))
            self.play(creature.blink())
        first_case2 = mn.MathTex(
            "a", "&=", f"{int(2022 / 3)}\\\\",
            "b", "&=", "2\\\\",
            "c", "&=", f"{int(2019 / 3)}",
            font_size=72
        )
        first_case2.set_color_by_tex_to_color_map({
            "a": mn.BLUE_D,
            "b": mn.BLUE,
            "c": mn.BLUE_B,
            f"{int(2022 / 3)}": mn.LIGHTER_GREY,
            "2": mn.LIGHTER_GREY,
            f"{int(2019 / 3)}": mn.LIGHTER_GREY
        })
        rec2 = mn.SurroundingRectangle(first_case2)
        mn.VGroup(first_case2, rec2).scale(5 / 6).to_edge(mn.RIGHT)
        with self.voiceover(f"Si lo hiciste bien, deberías obtener que a es {int(2022 / 3)}, b es igual a 2 y c es {int(2019 / 3)}"):
            self.play(mn.TransformMatchingTex(
                first_case, first_case2
            ))
            self.play(mn.Create(rec2))
            self.play(creature.eyes.anim_look_at(first_case2))
            self.play(creature.blink())
        with self.voiceover("El problema ya está terminado, así que es momento de despedirnos. Si les gustó el video, no olviden suscribirse, darle like y compartir. Nos vemos en el próximo video."):
            self.play(
                mn.FadeOut(*[m for m in self.mobjects if m != creature]),
                creature.eyes.anim_look(mn.ORIGIN)
            )
            self.play(creature.blink())
            self.wait()
            self.play(mn.FadeOut(creature.eyes))
            self.remove(creature.body)
            self.add(logo)
            self.play(mn.ShrinkToCenter(logo, path_arc=mn.PI / 2))
            self.wait()

            gracias_por_ver = mn.Tex("¡Gracias por ver!", font_size=72)
            gracias_por_ver.to_edge(mn.UP)
            self.play(mn.LaggedStartMap(
                mn.FadeIn, gracias_por_ver[0],
                shift=mn.UP / 2
            ))
            self.wait(20)

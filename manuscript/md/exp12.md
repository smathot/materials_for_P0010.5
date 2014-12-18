## Method

### Materials and availability

All experimental materials, where possible given license restrictions, are available from <https://github.com/smathot/materials_for_P0010.5>.

### Datasets, participants, procedure, and apparatus

We analyzed data from two previously unpublished experiments that were conducted for a different purpose. Data were independently collected and contained a mixture of different trial types. From Exp. 1 we analyzed only trials without any visible manipulation to the display (16 participants; 100 trials per participant). Exp. 1 was a difficult visual search task, in which participants searched for a small letter ('Z' or 'H'; 0.4°x0.4°) embedded in a natural scene. From Exp. 2, we analyzed all trials, which were a mixture of three task instructions (16 participants; 100 trials per participant; instruction varied between participants): A visual-search task, as in Exp. 1; A memory task, in which participants were (falsely) informed that they would be asked questions about the images; And a free-viewing task, in which no instructions were given. Eye movements were unconstrained.

Although the experiments were conducted at different locations, a similar experimental set-up was used. Eye movements were recorded monocularly with an EyeLink 1000, a video-based eye tracker sampling at 1000 Hz (SR Research, Mississauga, ON, Canada). Stimulus presentation was controlled by OpenSesame [@MathôtSchreijTheeuwes2012] using the PsychoPy back-end [@Peirce2007]. Observers participated in the experiments for course credit or money, reported normal or corrected vision, and signed a written consent form. The experiments were conducted with approval of the Ethics Board of the Faculty of Psychology and Education (VCWE; Exp. 1) and the local ethics committee of Aix-Marseille Université (Exp. 2).

### Stimuli, saliency maps, and pupillary luminance maps

In Exp. 1, stimuli were 200 photographs of natural scenes from the UPenn natural image database [@Tkačik2011]. Of these 200 stimuli, 100 were randomly selected for each participant. In Exp. 2, stimuli were 50 photographs of natural scenes from the Campus Scene collection [@BurgeGeisler2011], and 50 3D fractals generated with the program Mandelbulber [@Marczak2012].

%--
figure:
 id: FigMaps
 source: FigMaps.svg
 caption: |
  a) Participants freely viewed images of natural scenes or three-dimensional fractals. A small 'Z' or 'H' was hidden in each image and served as the target on visual-search trials. b) For each image, a pupillary luminance map was created to predict the pupillary light response for each location. c) A saliency map was created to predict where the eyes would land if gaze was guided purely by bottom-up visual saliency.
--%

### Saliency maps

For each image, we generated a saliency map, which is a best estimate of where the eyes would go if eye-movement guidance was purely bottom up (%FigMaps::a). Saliency maps were generated with the NeuroMorphic vision toolkit [@IttiKochNiebur1998], using the 'Surprise' visual-cortex model. Saliency maps were obtained with the following command:

	ezvision --just-initial-saliency-map --in=[input_filename] --out=png --vc-type=Surp --maxnorm-type=Surprise

### Pupillary luminance maps

For each image, we generated a pupillary luminance map, which is a best effort to predict pupil size for each fixation if pupil size was purely determined by luminance (%FigMaps::b). In other words, for each pixel in the image we estimated a value (in arbitrary units) that would predict pupil size during fixations on that pixel if only luminance were a factor.

It is clear that the pupillary light response (PLR) is driven primarily by foveal illumination, with an exponential drop-off in sensitivity with increasing eccentricity [@Crawford1936]. Based on data from a pupillometry study by @HongNarkiewiczKardon2001, we estimated the following relationship: *s* = 33.2+10.6∙e^-11.2\**ecc*^

Here *s* is pupil sensitivity (dB; a measure of the pupillary response to the light stimulus) and *ecc* is the eccentricity (°) of the light stimulus. However, @HongNarkiewiczKardon2001 probed a limited number of widely spaced locations and it is possible, if not likely, that the exponential drop-off in pupillary sensitivity that is observed in the wider visual field does not hold for the fovea. There is, to the best of our knowledge, no detailed mapping of pupillary sensitivity for the foveal area. We conducted a number of pilot experiments ourselves, which confirmed the general pattern observed by @HongNarkiewiczKardon2001 and @Crawford1936, but we failed to obtain a sufficiently clear foveal mapping to answer this question with any degree of certainty. Therefore, we applied Occam's razor and modeled the fovea as an area of 1° diameter with a uniform pupillary sensitivity. Non-foveal areas were modeled with the formula described above. Using this 'mixed luminance kernel', we first gray-scaled and then blurred the photos, thus obtaining pupillary luminance maps.

## Analysis

### Model selection

Like any set of data with unconstrained eye movements, our datasets contain many correlations that need to be taken into account when interpreting a relationship of interest, in our case between pupil size and the saliency of fixated locations (from now on: fixation saliency). For example, if high-salient locations would be brighter than low-salient locations, a light response would manifest itself as a pupillary constriction when fixating high-salient locations. (This is merely an example, see Supplementary Methods for the actual relationship between saliency and luminance.)

To deal with these correlations, we focus on the 'partial' relationship between pupil size and fixation saliency, i.e. the slope of the effect in a linear-mixed effects (LME) model that accounts for several other factors that might co-vary with pupil size. We used a combination of a data-driven and a confirmatory approach, in which we selected control predictors in a data-driven way, and used confirmatory testing for the effects of interest [see @Barr2013 for guidelines and a discussion].

More specifically, we started with a basic model with fixation saliency as dependent variable and a by-participant random intercept. Next, we progressively added the following control predictors as fixed effects: trial number, fixation number in trial, luminance of the fixated position (as read from the pupillary luminance map), eccentricity (distance between fixated position and display center), horizontal position, vertical position, fixation duration, and size of following saccade. Our choice of control predictors was not motivated by any theoretical interest, but served to account for as many factors as possible that might co-vary with pupil size. We did not include control predictors that correlated strongly with other control predictors, such as properties of preceding and following fixations (but see Temporal Characteristics). After adding each control predictor, we tested whether the addition improved the quality of the model, by determining *X*^2^ and the associated *p*-value from the log-likelihood of the two models [@BaayenDavidsonBates2008]. If the predictor significantly (*p* < .05) improved the model, it was included in the model, otherwise it was discarded.

Finally, after having constructed a model in this way, we added pupil size as fixed effect, as well as by-participant random slopes for pupil size. [More generally, we used random slopes only for predictors of theoretical interest, and not for control predictors, cf. @Barr2013]. Fixed effects were considered reliable when t > 2 [cf. @Baayen2008Introduction], although we will emphasize general patterns over significance of individual analyses. In the main text, we will describe only the effects of theoretical interest, but full LME models are listed in the Supplementary Methods.

### Pupil-size transformation

The power of an analysis can be increased (or reduced) by transforming variables. For example, when analyzing response times (RTs), statistical power often increases when a logarithmic or inverse transformation is applied to the RTs [@Ratcliff1993]. To our knowledge, the effect of transforming pupil-size measures has not been investigated. Most researchers use area [e.g., @Mathôt2014JVis;@Mathôt2013Plos] or diameter [e.g., @Binda2013JNeurosci] as dependent measure. Presumably (or certainly, for our own work) the chosen measure is driven by the default units of the eye tracker.

We used the data from Exp. 1 to determine the optimal pupil-size transformation.  First, we converted pupil size to *Z* scores, so that pupil-size measures were comparable between experiments (the EyeLink provides uncalibrated pupil-size measures that depend on the specifics of the set-up). Next, we constructed LME models as described above, adding pupil size as fixed effect after applying one of the following transformations: *D* (= diameter), *D*^2^ (= area), *D*^3^, *D*^0.5^, *D*^-1^, and log(*D*). This resulted in six models that differed only in the pupil-size transformation that was applied. Based on each model's log-likelihood, we selected the optimal transformation, i.e. from the model with the highest log-likelihood. This was the inverse transformation: *D*^-1^. Therefore, all subsequent analyses were performed after applying an inverse transformation to *Z* scored pupil-size diameter. (For details, see Supplementary Methods.)

## Results

### Trial duration and number of fixations

Trials lasted on average 12.6 s (Exp. 1) and 14.6 s (Exp. 2). The average fixation durations were 285 ms (Exp. 1) and 294 ms (Exp. 2). A total of 59,585 (Exp. 1) and 64,526 (Exp. 2) fixations were entered into the analyses. No participants or data points were excluded.

### Pupil size as a predictor of fixation saliency

The main result is that pupil size is related to fixation saliency: When the pupil is large, the average saliency of fixated locations is lower than when the pupil is small (%FigExp12Saccade). This effect is robust, present for the duration of a trial, and evident in both experiments (Exp. 1: *β* = 2.70, SE = 0.45, t = 5.93; Exp. 2: *β* = 1.56, SE = 0.48, t = 3.23). %FigExp12Saccade::b shows the relationship between pupil diameter and fixation saliency based on the grand mean of five pupil-diameter bins for Exp. 1. This figure shows that our partial-effect slopes (*β*), while based on complex analyses (as described above), reflect a real relationship that is clearly evident in the data.

%--
figure:
 id: FigExp12Saccade
 source: FigExp12Saccade.svg
 caption: |
  The partial effect (*β*) of pupil size (1/D) on fixation saliency (see text for details). a) The effect for both experiments across the entire dataset ('Full') and separately for the first twenty fixations. b) The shape of the relationship between fixation saliency and pupil diameter for Exp. 1. c) The effect for Exp. 2 split by stimulus type and task instruction. Error bands/ bars indicate standard errors.
--%

To investigate the effect of stimulus type and task instruction in Exp. 2, we added the interaction between pupil size and stimulus type, and between pupil size and task instruction to the LME model (see %FigExp12Saccade::b). We also added by-participant random slopes for the effects of task instruction and stimulus type. For simplicity, we did not include a three-way interaction. This model showed that the relationship between pupil size and fixation saliency was strongest for the visual search task (relative to free-viewing: *β* = 2.36, SE = 1.01, t = 2.32), with no reliable difference between the free-viewing and memory tasks (*β* = -0.35, SE = 0.99, t = 0.36). Furthermore, the relationship was stronger for scene than fractal stimuli (*β* = 1.27, SE = 0.28, t = 4.57). In other words, the relationship between pupil size and fixation saliency is generally present, but particularly pronounced during visual search and with familiar stimuli.

### Temporal characteristics

To investigate whether the relationship between fixation saliency and pupil size is temporally diffuse, we repeated the analysis described above but used fixation saliency for previous and next fixations as dependent measure. In other words, we tested whether pupil size at fixation *i* also predicts saliency at fixation *i*-2, *i*-1, *i*+1, etc. This was done using the same models as in the main analyses, but varying the dependent measure (fixation-saliency-2-back, fixation-saliency-1-back, etc.).

The outcome of this analysis is striking (%FigExp12Window): Pupil-size is strongly related to the saliency of the location that was just fixated. In general, there is a temporally diffuse window with a peak that is displaced by about one fixation. We believe that the width of this window reflects auto-correlations between measurements at different time points: Mental effort and pupil size fluctuate in cycles of several seconds [@Lowenstein1963Fatigue;@Reimer2014]. The fact that pupil size lags behind fixation saliency may reflect the latency of the pupillary response, which can be as low as 240 ms [@Mathôt2014JExp;@Beatty1982] or as high as 700 ms [@Mathôt2013Plos], depending on a range of factors.

%--
figure:
 id: FigExp12Window
 source: FigExp12Window.svg
 caption: |
   The partial effect (*β*) of pupil size (1/D) on fixation saliency as a function of various temporal displacements. A displacement of 1 on the x-axis corresponds to the relationship between pupil size on fixation *i*+1 and fixation saliency for fixation *i*. Error bands indicate standard errors.
--%

### Discussion

In summary, across two experiments we observed a relationship between pupil size and fixation saliency, such that you are more likely to look at low-salient locations when your pupil is relatively dilated. This relationship is not (fully) explained by any of the other variables that we considered. We interpret this relationship in terms of mental effort: Mental effort is required to engage top-down goals, and, if necessary, to overcome the inherent bottom-up bias towards high-salient locations. This interpretation is in line with the finding that the relationship between pupil size and fixation saliency was strongest in a visual-search task in which the target could be hidden anywhere, and observers therefore needed to look also at low-salient locations.

## Method

### Datasets, participants, procedure, and apparatus

We analyzed data from two previously unpublished experiments that were conducted for a different purpose. Data were independently collected and contained a mixture of different trial types. From Exp. 1 we analyzed only trials without any visible manipulation to the display (16 participants; 100 trials per participant). Exp. 1 was a difficult visual search task, in which participants searched for a small letter ('Z or 'H') embedded in a natural scene. From Exp. 2, we analyzed all trials, which were a mixture of three task instructions (16 participants; 100 trials per participant): A visual-search task, as in Exp. 1; A memory task, in which participants were (falsely) informed that they would be asked questions about the images; And a free-viewing task, in which no instructions were given. Eye movements were unconstrained.

In both experiments, eye movements were recorded with an EyeLink 1000, a video-based eye tracker sampling at 1000 Hz (SR Research, Mississauga, ON, Canada). Stimulus presentation was controlled by OpenSesame [@MathôtSchreijTheeuwes2012] using the PsychoPy back-end [@Peirce2007]. Observers participated in the experiments for course credit or money, reported normal or corrected vision, and signed a written consent form. The experiments were conducted with approval of the Ethics Board of the Faculty of Psychology and Education (VCWE; Exp. 1) and the local ethics committee of Aix-Marseille université (Exp. 2).

### Stimuli, saliency maps, and pupillary luminance maps

In Exp. 1, stimuli were 200 photographs of natural scenes from the UPenn natural image database [@Tkačik2011]. Of these 200 stimuli, 100 were randomly selected for each participant. In Exp. 2, stimuli were 50 photographs of natural scenes from the Campus Scene collection [@BurgeGeisler2011], and 50 3D fractals generated with the program Mandelbulber [@Marczak2012].

%--
figure:
 id: FigMaps
 source: sal-lum-maps.svg
 caption: |
  a) Participants freely viewed images of natural scenes or three-dimensional fractals. A small 'Z' or 'H' was hidden in each image and served as the target on visual-search trials. b) For each image, a pupillary luminance map was created to predict the pupillary light response for each location. c) A saliency map was created to predict where the eyes would land if gaze was guided purely by bottom-up visual saliency.
--%

### Saliency maps

For each image, we generated a saliency map, which is a best estimate of where the eyes would go, if only bottom-up factors would play a role in eye-movement guidance (%FigMaps::a). Saliency maps were generated with the NeuroMorphic vision toolkit [@IttiKochNiebur1998], using the 'Suprise' visual-cortex model. Saliency maps were obtained with the following command:

	ezvision --just-initial-saliency-map --in=[input_filename] --out=png --vc-type=Surp --maxnorm-type=Surprise

### Pupillary luminance maps

For each image, we generated a pupillary luminance map, which is a best effort to predict pupil size for each fixation, if only luminance was a factor (%FigMaps::b). For each pixel in the image, we estimated a value (in arbitrary units) that would predict pupil size during fixations on that pixel if only luminance were a factor.

It has been long known that the PLR is driven primarily by foveal illumination, with an exponential drop-off in sensitivity with increasing eccentricity [@Crawford1936]. Based on data from a pupillometry study by @HongNarkiewiczKardon2001, we estimated the following relationship: `s = 33.2+10.6*e^-11.2*ecc^`. Here `s` is pupil sensitivity (dB; a measure of the pupillary response to the light stimulus) and `ecc` is the eccentricity (°) of the light stimulus. However, @HongNarkiewiczKardon2001 probed a limited number of widely spaced locations and it is possible, if not likely, that the exponential drop-off in pupillary sensitivity that is observed in the wider visual field does not hold for fovea. There is, to the best of our knowledge, no detailed mapping of pupillary sensitivity for the foveal area. We conducted a number of pilot experiments, which confirmed the general pattern observed by @HongNarkiewiczKardon2001 and @Crawford1936, but we failed to obtain a sufficiently clear foveal mapping to answer this question with any degree of certainty. Therefore, we applied Occam's razor and modeled the fovea as an area of 1° diameter with a uniform pupillary sensitivity. Non-foveal areas were modeled with the formula described above. Using this 'mixed luminance kernel', we first gray-scaled and then blurred the photos, thus obtaining pupillary luminance maps.

## Analysis and results

### Trial duration and number of fixations

Trials lasted on average 12.6 s (Exp. 1) and 14.6 s (Exp. 2). The average fixation durations were 272 ms (Exp. 1) and 283 ms (Exp. 2). A total of 59.706 (Exp. 1) and 64.622 (Dataset 2) fixations were entered into the analyses. No participants or data points were excluded.

### Pupil size as a predictor of fixation saliency

The main result is that pupil size correlates with the visual saliency of the fixated location (fixation saliency): When the pupil is large, the chance of fixating a low-salient location is larger than when the pupil is small. This effect is robust, present for the duration of a trial, and evident in both experiments (%FigCorpusMain).

%--
figure:
 id: FigCorpusMain
 source: corpus-main.svg
 caption: |
  The relationship between pupil size and saliency of fixated locations. The dependent variable is the slope of the partial relationship between pupil size and saliency given the model described in the main text. a) The effect for both experiments across the entire dataset ('Full') and separately for the first twenty fixations. b) The effect for Exp. 2 split by stimulus type and task instruction. Error bands/ bars indicate 95% confidence intervals.
--%

Like any set of free-viewing eye-movement data, our datasets contain many correlations that need to be taken into account when interpreting relationships. For example, if high-salient locations would be brighter than low-salient locations, a light response would manifest itself as a pupillary constriction when fixating high-salient locations. (This is merely an example, see Supplementary Methods for the actual relationship between saliency and luminance.)

To deal with these correlations, we consider the 'partial' relationship between pupil size and fixation saliency, i.e. the variance in fixation saliency that is uniquely explained by pupil size. We also present the direct relationship (i.e. without taking into account other variables) for the main analyses, to ascertain that the patterns of interest are actually present in the data, and are not artifacts of our statistical model [for a related discussion, see @WurmFisicaro2014].

For both experiments, we conducted the following analysis. We started with a linear mixed-effects model with fixation saliency (i.e. the saliency of the fixated location as read out of the saliency map) as dependent measure, and participant as a random effect on the intercept and slope. Starting from this basic model, we progressively added the following predictors as fixed effects: trial number, fixation number in trial, luminance of the fixated position (as read from the pupillary luminance map), eccentricity (distance of fixated position from the display center), horizontal position, vertical position, fixation duration, and size of following saccade.

Our choice of predictors was not motivated by a theoretical interest in these predictors per se, but served to account for as many factors as possible that might co-vary with both fixation saliency and pupil size. We did not include predictors that correlated strongly with other predictors, such as properties of preceding and following fixations (but see [Temporal Characteristics]).

After adding each predictor, we tested whether the addition improved the quality of the model, by determining X^2^ and the associated *p*-value from the log-likelihood of the two models [@BaayenDavidsonBates2008]. If the predictor significantly (*p* < .05) improved the model, it was included in the model, otherwise it was discarded (for details, see Supplementary Methods). Fixed effects were considered significant when t > 2 [cf. @Baayen2008Introduction].

After having constructed a model in this way we tested whether adding pupil size as fixed effect significantly improved the model. This was the case in both datasets (Exp. 1: X2(1) = 15.9, p < .001; Exp. 2: X2(1) = 8.5, p = .004) and there was both a partial (Exp. 1: t = 4.92; Exp. 2: t = 3.23) and direct (Exp. 1: t = 5.11; Exp. 2: t = 3.46) relationship between pupil size and fixation saliency. In other words, pupil size predicts fixation saliency, and this is not (fully) driven by any of the other factors that we considered.

A break-down by task instruction and stimulus type for Exp. 2 suggests that the effect is general, although it was most pronounced for the visual-search task (%FigCorpusMain::b). We will address the effect of task instruction more systematically in [Experiment 3].

### Temporal characteristics

To investigate whether or not the relationship between fixation saliency and pupil size is temporally diffuse, we repeated the analysis described above but used fixation saliency for previous and next fixations as dependent measure. In other words, we tested whether pupil size at fixation i also predicts saliency at fixation i-2, i-1, i+1, etc. The outcome of this analysis is striking (%FigCorpusWindow): Pupil-size is most strongly related to the saliency of the location that was just fixated--more so than of the currently fixated location. In general, there is a temporally diffuse window with a peak that is displaced by one fixation. One possibility is that this reflects a gradual fluctuation of mental effort, which is unlikely to change abruptly from one fixation to the next. The fact that pupil size 'lags behind' fixation saliency may reflect the latency of the pupillary response, which can be as low as 200 ms [@Beatty1982] or as high as 700 ms [@MathôtVan+der+lindenGraingerVitu2013], depending on a range of factors.

%--
figure:
 id: FigCorpusWindow
 source: corpus-window.svg
 caption: "The relationship between pupil size and fixation saliency for various temporal displacements. A displacement of 1 on the x-axis corresponds to the relationship between pupil size on fixation `i+1` and fixation saliency for fixation `i`. The y-axis reflects the partial-effect slope of pupil size on fixation saliency. Error bands indicate 95% confidence intervals."
--%

### Discussion

In summary, across two experiments we observed a relationship between pupil size and fixation saliency, such that you are more likely to look at low-salient locations when you're pupil is relatively constricted. This relationship is not (fully) explained by any of the other variables that we considered. We interpret this relationship in terms of mental effort: Mental effort is required in order to overcome the inherent bias to fixate high-salient locations.


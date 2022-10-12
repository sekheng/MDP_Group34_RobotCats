package com.example.robotcatmobile.home_parts;

import android.os.Build;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.widget.AppCompatToggleButton;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioGroup;

import com.example.robotcatmobile.R;

@RequiresApi(api = Build.VERSION_CODES.N)
public class Frag_SetObs extends Fragment {
    // radio group for obstacles
    RadioGroup mToggleGroups;

    public Frag_SetObs() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_set_obs, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        mToggleGroups = view.findViewById(R.id.toggle_groups);

        for (int j = 0; j < mToggleGroups.getChildCount(); j++) {
            final AppCompatToggleButton toggleButton = (AppCompatToggleButton) mToggleGroups.getChildAt(j);
            toggleButton.setOnCheckedChangeListener((compoundButton, b) -> {
                        String toggleButtonTxt = compoundButton.getText().toString();
                        if (b) {
                            for (int i = 0; i < mToggleGroups.getChildCount(); i++) {
                                final AppCompatToggleButton otherToggle = (AppCompatToggleButton)mToggleGroups.getChildAt(i);
                                if (compoundButton != otherToggle)
                                    otherToggle.setChecked(false);
                            }
                            // then set the state
                            for (SET_GRID_STATE state:SET_GRID_STATE.values()) {
                                if (toggleButtonTxt.contains(state.toString())) {
                                    GridRecycler.curInteractState = state;
                                    break;
                                }
                            }
                        }
                        else {
                            // then check and ensure that the buttons matched with the undex
                            if (toggleButtonTxt.contains(GridRecycler.curInteractState.toString()))
                            {
                                GridRecycler.curInteractState = SET_GRID_STATE.NONE;
                            }
                        }
                    }
            );
        }
    }
}